from typing import Dict, Any, List
from src.candidate.schemas import CvEvaluation, ProjectEvaluation
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import re
from openai import OpenAI

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8),retry=retry_if_exception_type(Exception))
def _call_llm(llm: OpenAI, messages: List[Dict[str, str]], model: str = "mistralai/mistral-7b-instruct", temperature: float = 0.3) -> str:
    resp = llm.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=400
    )
    return resp.choices[0].message.content


def _safe_parse_json(text: str) -> Dict[str, Any]:
    try:
        # first try direct parse
        return json.loads(text)
    except Exception:
        # try to extract with regex
        match = re.search(r"\{(?:.|\s)*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                # attempt some naive fixes: replace single quotes, trailing commas
                cleaned = match.group(0).replace("'", '"')
                cleaned = re.sub(r",\s*}", "}", cleaned)
                cleaned = re.sub(r",\s*]", "]", cleaned)
                try:
                    return json.loads(cleaned)
                except Exception:
                    return {}
        return {}

def generate_overall_summary(cv_eval: CvEvaluation, project_eval: ProjectEvaluation , llm : OpenAI) -> str:
    prompt = f"""
        SYNTHESIZE a 3-5 sentence summary for this candidate, focusing on:
        - top strengths
        - main gaps
        - short recommendation (hire / consider / not recommended)

        CV scores & feedback:
        {cv_eval.model_dump()}

        Project scores & feedback:
        {project_eval.model_dump()}
    """
    content = _call_llm(llm, messages=[{"role": "user", "content": prompt}], temperature=0.35)
    # keep only first paragraph & trim
    return content.strip().split("\n\n")[0][:800]

def evaluate_project_with_llm(report_text: str, context: str, llm : OpenAI) -> Dict[str, Any]:
    prompt = f"""
        You are an assistant that scores project reports for a backend case-study.

        REFERENCE (use when scoring):
        {context}

        PROJECT REPORT:
        {report_text}

        Task:
        1) For each parameter below, give an integer score between 1 and 5.
        - correctness (prompt design, chaining, RAG, handling errors)
        - code_quality (clean, modular, testable)
        - resilience (handles failures, retries)
        - documentation (README, explanations)
        - creativity (bonus features)

        2) Provide a short feedback string (1-2 sentences).

        Output must be valid JSON EXACTLY in this format:
        {{
        "correctness": <int 1-5>,
        "code_quality": <int 1-5>,
        "resilience": <int 1-5>,
        "documentation": <int 1-5>,
        "creativity": <int 1-5>,
        "feedback": "<brief feedback>"
        }}
    """
    content = _call_llm(llm, messages=[{"role": "user", "content": prompt}], temperature=0.18)
    parsed = _safe_parse_json(content)
    return {
        "correctness": int(parsed.get("correctness", 1)),
        "code_quality": int(parsed.get("code_quality", 1)),
        "resilience": int(parsed.get("resilience", 1)),
        "documentation": int(parsed.get("documentation", 1)),
        "creativity": int(parsed.get("creativity", 1)),
        "feedback": parsed.get("feedback", "").strip()
    }

def evaluate_cv_with_llm(cv_text: str, context: str, llm : OpenAI) -> Dict[str, Any]:
    prompt = f"""
        You are an assistant that scores candidate CVs for a Backend Product Engineer role.

        REFERENCE (use when scoring):
        {context}

        CANDIDATE CV:
        {cv_text}

        Task:
        1) For each parameter below, give an integer score between 1 and 5.
        - technical_skills (backend, databases, APIs, cloud, AI/LLM exposure)
        - experience_level (years, project complexity)
        - achievements (impact, scale)
        - cultural_fit (communication, learning attitude)

        2) Provide a short feedback string (1-2 sentences).

        Output must be valid JSON EXACTLY in this format:
        {{
        "technical_skills": <int 1-5>,
        "experience_level": <int 1-5>,
        "achievements": <int 1-5>,
        "cultural_fit": <int 1-5>,
        "feedback": "<brief feedback>"
        }}
    """
    content = _call_llm(llm,messages=[{"role": "user", "content": prompt}], temperature=0.15)
    parsed = _safe_parse_json(content)
    return {
        "technical_skills": int(parsed.get("technical_skills", 1)),
        "experience_level": int(parsed.get("experience_level", 1)),
        "achievements": int(parsed.get("achievements", 1)),
        "cultural_fit": int(parsed.get("cultural_fit", 1)),
        "feedback": parsed.get("feedback", "").strip()
    }