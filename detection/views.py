import os
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.cluster import KMeans
import joblib

# Global variables
UPLOAD_DIR = "uploads"
MODEL_PATH = r"C:\Users\Dell\OneDrive\Desktop\FakeRatingDetection (2)\FakeRatingDetection\AIModel\kmeans_model.pkl"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@csrf_exempt
def upload_files(request):
    if request.method == "POST":
        files = request.FILES
        for name, file in files.items():
            with open(os.path.join(UPLOAD_DIR, name), 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
        return JsonResponse({"message": "Files uploaded successfully."})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def train_model(request):
    if request.method == "POST":
        # Process the uploaded files
        try:
            user_rating_file = os.path.join(UPLOAD_DIR, "user_rating.txt")
            mc_file = os.path.join(UPLOAD_DIR, "mc.txt")
            rating_file = os.path.join(UPLOAD_DIR, "rating.txt")

            # Read and process data
            user_rating_df = pd.read_csv(user_rating_file, sep="\t", header=None,
                                         names=["MY_ID", "OTHER_ID", "VALUE", "CREATION"])
            ratings_df = pd.read_csv(rating_file, sep="\t", header=None,
                                     names=["OBJECT_ID", "MEMBER_ID", "RATING", "STATUS", "CREATION", "LAST_MODIFIED", "TYPE", "VERTICAL_ID"])

            # Fix invalid ratings
            ratings_df['RATING'] = ratings_df['RATING'].apply(lambda x: 5 if x == 6 else x)

            # Merge for clustering
            features = ratings_df[["RATING"]].fillna(0)

            # Train the model
            kmeans = KMeans(n_clusters=2, random_state=42)
            kmeans.fit(features)

            # Save the model
            joblib.dump(kmeans, MODEL_PATH)

            return JsonResponse({"message": "Model trained successfully."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def predict(request):
    if request.method == "POST":
        # Load the model
        if not os.path.exists(MODEL_PATH):
            return JsonResponse({"error": "Model not trained yet."}, status=400)

        kmeans = joblib.load(MODEL_PATH)

        # Process new data
        try:
            data = pd.read_json(request.body.decode('utf-8'))
            features = data[["RATING"]].fillna(0)

            # Predict clusters
            predictions = kmeans.predict(features)
            data['Cluster'] = predictions

            return JsonResponse(data.to_dict(orient='records'), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
