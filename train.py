import pandas as pd
from surprise import Reader, Dataset, SVD
import pickle

print("1. Loading the MovieLens dataset...")
# Load only the columns we need to save memory
ratings = pd.read_csv('ratings.csv', usecols=['userId', 'movieId', 'rating'])

print("2. Preparing the data for the brain...")
# Tell the model our ratings go from 0.5 to 5.0 stars
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings, reader)
trainset = data.build_full_trainset()

print("3. Training the SVD model (Matrix Factorization)...")
algo = SVD()
algo.fit(trainset)

print("4. Saving the trained brain to a file...")
# We use 'pickle' to pack up the trained model so FastAPI can use it later
with open('svd_model.pkl', 'wb') as f:
    pickle.dump(algo, f)

print("Done! You now have a trained model file.")