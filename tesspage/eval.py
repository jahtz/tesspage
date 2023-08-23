import dinglehopper
from rapidfuzz.distance import Levenshtein


def evaluate_cer(ground_truth: str, prediction: str) -> float:
    """
    Calculates Character Error Rate (CER)

    Args:
        ground_truth: ground truth string
        prediction: prediction string

    Returns:
        cer float
    """
    return dinglehopper.character_error_rate(ground_truth, prediction)


def evaluate_wer(ground_truth: str, prediction: str) -> float:
    """
    Calculates Word Error Rate (WER)

    Args:
        ground_truth: ground truth string
        prediction: prediction string

    Returns:
        wer float
    """
    return dinglehopper.word_error_rate(ground_truth, prediction)


def levenshtein_distance(ground_truth: str, prediction: str) -> int:
    """
    Calculates Levenshtein Distance

    Args:
        ground_truth: ground truth string
        prediction: prediction string

    Returns:
        distance int
    """
    return Levenshtein.distance(ground_truth, prediction)
