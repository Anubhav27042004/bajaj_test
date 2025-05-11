import requests

url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
payload = {
    "name": "John Doe",
    "regNo": "REG12347",
    "email": "john@example.com"
}
response = requests.post(url, json=payload)

if response.status_code != 200:
    raise Exception("Failed to generate webhook: " + response.text)


data = response.json()
webhook_url = data["webhook"]
access_token = data["accessToken"]

solution_sql_query = """
SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURDATE(), e.DOB) / 365) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE 
    DAY(p.PAYMENT_TIME) != 1 
    AND p.AMOUNT = (
        -- find the maximum salary paid (not on 1st day)
        SELECT MAX(AMOUNT)
        FROM PAYMENTS
        WHERE DAY(PAYMENT_TIME) != 1
    );

"""

# Submitting the solution to the webhook
submit_response = requests.post(
    webhook_url,
    headers={"Authorization": data["accessToken"], "Content-Type": "application/json"},
    json={"finalQuery": solution_sql_query.strip()}
)

if submit_response.status_code == 200:
    print("Query submitted successfully.")
else:
    print("Submission failed:", submit_response.text)