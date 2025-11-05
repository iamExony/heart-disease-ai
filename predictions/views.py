
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .ml_model.clinical_mlp import MLPModel
import torch, joblib, numpy as np, os, shap
import pandas as pd
from .models import Prediction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_clinical(request):
    try:
        # --- Feature setup ---
        features = [
            "bp","HighChol","CholCheck","BMI","Smoker","Stroke","Diabetes","PhysActivity",
            "Fruits","Veggies","HvyAlcoholConsump","AnyHealthcare","NoDocbcCost","GenHlth",
            "MentHlth","PhysHlth","DiffWalk","Sex","Age","Education","Income"
        ]

        # --- Prepare input ---
        data = request.data
        input_data = np.array([[data[f] for f in features]], dtype=float)

        # --- Load model and scaler ---
        scaler_bundle = joblib.load(os.path.join("predictions/ml_model/scaler.pkl"))
        scaler = scaler_bundle["scaler"]
        features = scaler_bundle["features"]
        model = MLPModel(input_dim=len(features))
        model.load_state_dict(torch.load("predictions/ml_model/mlp_model.pt", map_location=torch.device("cpu")))
        model.eval()

        # --- Scale input ---
        input_df = pd.DataFrame([input_data[0]], columns=features)
        scaled = scaler.transform(input_df)
        tensor_data = torch.tensor(scaled, dtype=torch.float32)

        # --- Predict probability ---
        with torch.no_grad():
            logits = model(tensor_data)
            prob = float(torch.sigmoid(logits).item())
            risk_class = int(prob > 0.5)

        message = "High likelihood of cardiovascular disease" if risk_class == 1 else "Low likelihood of cardiovascular disease"

        # --- SHAP explainability ---
        background_path = "predictions/ml_model/shap_background.pkl"
        shap_values = None
        top_features = []

        if os.path.exists(background_path):
            background = joblib.load(background_path)
            # Ensure background is torch tensor
            if not isinstance(background, torch.Tensor):
                background_tensor = torch.tensor(background, dtype=torch.float32)
            else:
                background_tensor = background.detach().clone()
            explainer = shap.DeepExplainer(model, background_tensor)
            shap_out = explainer.shap_values(tensor_data)
            # shap_out may be a list (for single-output models) containing numpy arrays
            # or torch tensors depending on the explainer/backend. Normalize to a numpy array.
            if isinstance(shap_out, (list, tuple)):
                raw_shap = shap_out[0][0] if len(shap_out) > 0 and len(shap_out[0]) > 0 else shap_out[0]
            else:
                # shap_out already an array-like for the first output
                raw_shap = shap_out[0]

            if isinstance(raw_shap, torch.Tensor):
                shap_values = raw_shap.detach().cpu().numpy()
            else:
                # If it's already a numpy array or list-like, convert to numpy
                shap_values = np.array(raw_shap)

            # Pair feature names with SHAP impacts
            feature_impacts = list(zip(features, shap_values))
            feature_impacts.sort(key=lambda x: abs(x[1]), reverse=True)

            top_features = [
                {"feature": name, "impact": round(float(value), 4)}
                for name, value in feature_impacts[:5]
            ]

        # --- Final response ---

        # Store prediction in DB
        pred_obj = Prediction.objects.create(
            user=request.user,
            input_data=data,
            result={
                "risk_probability": round(prob, 3),
                "risk_class": risk_class,
                "message": message,
                "top_features": top_features
            }
        )

        return Response(pred_obj.result)

    except Exception as e:
        return Response({"error": str(e)})
