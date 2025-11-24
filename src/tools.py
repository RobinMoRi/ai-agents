from agno.tools import tool


@tool(
    name="LatestPaymentStatusTool",
    description="Get latest payment status from third party system",
)
def get_latest_payment_status(client_id: int):
    return {"status": "CONFIRMED", "client_id": client_id}
