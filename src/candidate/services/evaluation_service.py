
from fastapi import Depends, BackgroundTasks
from typing import List
from src.candidate.repositories.candidate_repository import CandidateRepositoryProtocol
from src.dependencies import get_candidate_repository
from openai import OpenAI
from src.config import settings
import json
from src.candidate.schemas import CvEvaluation, ProjectEvaluation

from src.candidate.utils.file_utils import extract_text_from_pdf
from src.candidate.utils.rag_utils import retrieve_context
from src.candidate.utils.ai_utils import evaluate_cv_with_llm , evaluate_project_with_llm, generate_overall_summary

from src.vectordb import get_chroma_collection

class EvaluationService:

    def __init__(self, repository : CandidateRepositoryProtocol = Depends(get_candidate_repository)) -> None:
        self.repository = repository
        self.llm_client = OpenAI(
            base_url = settings.LLM_BASE_URL,
            api_key = settings.LLM_CLIENT_API_TOKEN
        )

        self.cv_weights = {
            "technical_skills": 0.40,
            "experience_level": 0.25,
            "achievements": 0.20,
            "cultural_fit": 0.15,
        }
        self.project_weights = {
            "correctness": 0.30,
            "code_quality": 0.25,
            "resilience": 0.20,
            "documentation": 0.15,
            "creativity": 0.10,
        }

    def evaluate(self, candidate_ids: List[int], background_tasks:  BackgroundTasks) -> None:
        for candidate_id in candidate_ids:
            background_tasks.add_task(
                self._process_evaluation,
                candidate_id
            )

    def _process_evaluation(self, candidate_id: int):
        try:
            print(f"🔍 Evaluating candidate {candidate_id}...")
            self._process_sync(candidate_id)
        except Exception as exc:
            self.repository.update(candidate_id, {
                "status": "FAILED",
                "error": str(exc)
            })

        print(f"✅ Finished evaluating candidate {candidate_id}.")

    def _process_sync(self, candidate_id: int):
        candidate = self.repository.find_by_id(candidate_id)
        if not candidate:
            return

        self.repository.update(candidate_id, {
            "status": "PROCESSING",
            "evaluation_result_json": None,
            "error": None
        })

        cv_paths = candidate.cv_paths
        project_report_paths = candidate.project_report_paths
        if not cv_paths or not project_report_paths:
            raise ValueError("Missing cv_paths or project_report_paths in candidate record")

        print("📄 Extracting text from CV and Project Report...")
        cv_text = extract_text_from_pdf(cv_paths)
        report_text = extract_text_from_pdf(project_report_paths)

        print("🧠 Retrieving context from VectorDB...")
        cv_context = retrieve_context(get_chroma_collection(), "job description backend developer cv rubric", n=3)
        project_context = retrieve_context(get_chroma_collection(), "case study brief project rubric", n=4)


        print("🤖 Evaluating with LLM...")
        cv_eval_raw = evaluate_cv_with_llm(cv_text, cv_context, self.llm_client)
        cv_eval = CvEvaluation(**cv_eval_raw)
        cv_eval.calculate_match_rate(self.cv_weights)

        print("🤖 Evaluating project with LLM...")
        project_eval_raw = evaluate_project_with_llm(report_text, project_context, self.llm_client)
        project_eval = ProjectEvaluation(**project_eval_raw)
        project_eval.calculate_final_score(self.project_weights)

        print("📝 Generating overall summary...")
        overall_summary = generate_overall_summary(cv_eval, project_eval, self.llm_client)

        result_payload = {
            "cv_match_rate": cv_eval.match_rate,
            "cv_feedback": cv_eval.feedback,
            "cv_breakdown": cv_eval.model_dump(),
            "project_score": project_eval.final_score,
            "project_feedback": project_eval.feedback,
            "project_breakdown": project_eval.model_dump(),
            "overall_summary": overall_summary,
        }

        print("💾 Updating candidate record with evaluation results...")
        self.repository.update(candidate_id, {
            "status": "COMPLETED",
            "evaluation_result_json": json.dumps(result_payload, ensure_ascii=False)
        })

        print("✅ Candidate evaluation completed and saved.")
        