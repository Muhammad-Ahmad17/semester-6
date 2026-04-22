# Simple Linear Regression using Gradient Descent

## Mathematical Model to Code Explanation

---

## 1. Linear Regression Model

### Mathematical Formula:
```
ŷ = b₀ + b₁ · x
```

Where:
- `ŷ` = predicted value (Salary)
- `x` = input feature (Years of Experience)
- `b₀` = intercept (bias)
- `b₁` = slope (weight)

### Code Implementation:
```python
y_pred = b0 + b1 * x
```

---

## 2. Cost Function (Mean Squared Error)

### Mathematical Formula:
```
J(b₀, b₁) = (1/n) × Σᵢ₌₁ⁿ (ŷᵢ - yᵢ)²
```

This measures how far our predictions are from actual values.

### Code Implementation:
```python
error = y_pred - y
cost = (1/n) * np.sum(error ** 2)
```

---

## 3. Gradient Descent Algorithm

The goal is to minimize the cost function by updating parameters in the direction of steepest descent.

### Partial Derivatives (Gradients):

**Gradient with respect to b₀:**
```
∂J/∂b₀ = (2/n) × Σᵢ₌₁ⁿ (ŷᵢ - yᵢ)
```

**Gradient with respect to b₁:**
```
∂J/∂b₁ = (2/n) × Σᵢ₌₁ⁿ (ŷᵢ - yᵢ) × xᵢ
```

### Code Implementation:
```python
gradient_b0 = (2/n) * np.sum(error)
gradient_b1 = (2/n) * np.sum(error * x)
```

---

## 4. Parameter Update Rule

### Mathematical Formula:
```
b₀ = b₀ - α × ∂J/∂b₀
b₁ = b₁ - α × ∂J/∂b₁
```

Where `α` (alpha) is the learning rate.

### Code Implementation:
```python
b0 = b0 - learning_rate * gradient_b0
b1 = b1 - learning_rate * gradient_b1
```

---

## 5. Complete Algorithm Flow

```
1. Initialize: b₀ = 0, b₁ = 0
2. Repeat for n iterations:
   a. Compute predictions: ŷ = b₀ + b₁ × x
   b. Compute error: error = ŷ - y
   c. Compute gradients:
      - ∂J/∂b₀ = (2/n) × Σ(error)
      - ∂J/∂b₁ = (2/n) × Σ(error × x)
   d. Update parameters:
      - b₀ = b₀ - α × ∂J/∂b₀
      - b₁ = b₁ - α × ∂J/∂b₁
3. Return b₀, b₁
```

---

## 6. Feature Normalization

### Why Normalize?
- Gradient descent converges faster with normalized features
- Prevents features with larger scales from dominating

### Formula:
```
x_normalized = (x - μₓ) / σₓ
y_normalized = (y - μᵧ) / σᵧ
```

Where:
- `μ` = mean
- `σ` = standard deviation

### Code:
```python
x_norm = (x - x_mean) / x_std
y_norm = (y - y_mean) / y_std
```

### Converting Back to Original Scale:
After training on normalized data:
```python
b1_original = (y_std * b1_normalized) / x_std
b0_original = y_mean + y_std * b0_normalized - b1_original * x_mean
```

---

## 7. Evaluation Metrics

### Mean Absolute Error (MAE):
```
MAE = (1/n) × Σᵢ₌₁ⁿ |yᵢ - ŷᵢ|
```
```python
mae = np.sum(np.abs(y - y_pred)) / n
```

### Root Mean Square Error (RMSE):
```
RMSE = √[(1/n) × Σᵢ₌₁ⁿ (yᵢ - ŷᵢ)²]
```
```python
rmse = np.sqrt(np.sum((y - y_pred) ** 2) / n)
```

### R² Score (Coefficient of Determination):
```
R² = 1 - [Σ(yᵢ - ŷᵢ)² / Σ(yᵢ - ȳ)²]
```
```python
r2 = 1 - (np.sum((y - y_pred) ** 2) / np.sum((y - y_mean) ** 2))
```

---

## Summary Table

| Mathematical Concept | Formula | Python Code |
|---------------------|---------|-------------|
| Prediction | ŷ = b₀ + b₁x | `y_pred = b0 + b1 * x` |
| Error | e = ŷ - y | `error = y_pred - y` |
| MSE Cost | J = (1/n)Σe² | `cost = (1/n) * np.sum(error**2)` |
| Gradient b₀ | (2/n)Σe | `(2/n) * np.sum(error)` |
| Gradient b₁ | (2/n)Σ(e×x) | `(2/n) * np.sum(error * x)` |
| Update b₀ | b₀ - α×∂J/∂b₀ | `b0 - learning_rate * grad_b0` |
| Update b₁ | b₁ - α×∂J/∂b₁ | `b1 - learning_rate * grad_b1` |

---

**Author:** Muhammad Ahmad (FA23-BCE-113)  
**Course:** CSC462 - Artificial Intelligence
