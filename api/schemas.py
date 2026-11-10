"""Request/response shapes. FastAPI uses these to validate every request."""
from typing import Literal

from pydantic import BaseModel, Field


class Customer(BaseModel):
    tenure: int = Field(..., ge=0, le=100, description="Months with the company")
    MonthlyCharges: float = Field(..., ge=0)
    TotalCharges: float = Field(..., ge=0)
    SeniorCitizen: Literal[0, 1]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    PaymentMethod: Literal["Electronic check", "Mailed check",
                           "Bank transfer (automatic)", "Credit card (automatic)"]
    PaperlessBilling: Literal["Yes", "No"]
    TechSupport: Literal["Yes", "No", "No internet service"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "tenure": 2, "MonthlyCharges": 85.5, "TotalCharges": 171.0,
                "SeniorCitizen": 0, "Contract": "Month-to-month",
                "InternetService": "Fiber optic", "PaymentMethod": "Electronic check",
                "PaperlessBilling": "Yes", "TechSupport": "No",
            }
        }
    }


class Prediction(BaseModel):
    churn: bool
    churn_probability: float
