
# Train the models using the module we just created
from models import train_and_save_models

# Train and save models
predictor, results = train_and_save_models('synthetic_mining_data.csv')
