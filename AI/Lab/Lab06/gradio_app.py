# fa23-bce-098
# UZAIR

import numpy as np
import pandas as pd
import gradio as gr
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load and prepare data
df = pd.read_csv('50_Startups.csv')
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)

# Train Linear Regression
model1 = LinearRegression()
model1.fit(X_train, y_train)
y_pred_test1 = model1.predict(X_test)
mae_lr = mean_absolute_error(y_test, y_pred_test1)

# Train Decision Tree
model2 = tree.DecisionTreeRegressor(max_depth=2, random_state=3)
model2.fit(X_train, y_train)
y_pred_test2 = model2.predict(X_test)
mae_dt = mean_absolute_error(y_test, y_pred_test2)

# Train Random Forest
model3 = RandomForestRegressor(random_state=3)
model3.fit(X_train, y_train)
y_pred_test3 = model3.predict(X_test)
mae_rf = mean_absolute_error(y_test, y_pred_test3)

def predict_profit(rd_spend, administration, marketing_spend):
    """
    Predict startup profit using three different regression models
    """
    # Prepare input
    input_data = np.array([[rd_spend, administration, marketing_spend]])

    # Get predictions from all models
    pred_lr = model1.predict(input_data)[0]
    pred_dt = model2.predict(input_data)[0]
    pred_rf = model3.predict(input_data)[0]

    # Format results
    results = f"""
    **Prediction Results:**

    **Linear Regression:**
    - Predicted Profit: ${pred_lr:,.2f}
    - Test MAE: ${mae_lr:,.2f}

    **Decision Tree:**
    - Predicted Profit: ${pred_dt:,.2f}
    - Test MAE: ${mae_dt:,.2f}

    **Random Forest (Best Model):**
    - Predicted Profit: ${pred_rf:,.2f}
    - Test MAE: ${mae_rf:,.2f}

    **Recommendation:** Random Forest typically provides the most accurate prediction with the lowest MAE.
    """

    return results

# Create Gradio interface
with gr.Blocks(title="Startup Profit Predictor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Startup Profit Predictor
    **fa23-bce-098 | UZAIR**

    ### Compare predictions from three regression algorithms
    Enter the startup's spending data to predict potential profit.
    """)

    with gr.Row():
        with gr.Column():
            rd_spend = gr.Number(
                label="R&D Spend ($)",
                value=165349.20,
                info="Research and Development spending"
            )
            administration = gr.Number(
                label="Administration ($)",
                value=136897.80,
                info="Administrative costs"
            )
            marketing_spend = gr.Number(
                label="Marketing Spend ($)",
                value=471784.10,
                info="Marketing and advertising costs"
            )

            predict_btn = gr.Button("Predict Profit", variant="primary")

        with gr.Column():
            output = gr.Markdown(label="Results")

    predict_btn.click(
        fn=predict_profit,
        inputs=[rd_spend, administration, marketing_spend],
        outputs=output
    )

    gr.Markdown("""
    ---
    ### Model Information:
    - **Linear Regression**: Simple linear relationship model
    - **Decision Tree**: Tree-based decision model (max_depth=2)
    - **Random Forest**: Ensemble of decision trees (best performance)

    Dataset: 50 Startups with R&D Spend, Administration, and Marketing Spend features
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)  # share=True creates a public link