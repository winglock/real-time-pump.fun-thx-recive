import json
import os
from collections import defaultdict

# 데이터 폴더 및 파일 설정
data_folder = "data"
all_data = []

# JSON 파일 불러오기
for filename in os.listdir(data_folder):
    if filename.endswith(".json"):
        with open(os.path.join(data_folder, filename), "r", encoding="utf-8") as f:
            file_data = json.load(f)
            if "Solana" in file_data and "DEXTrades" in file_data["Solana"]:
                all_data.extend(file_data["Solana"]["DEXTrades"])

# 토큰별 거래량 누적 변수 및 단일 거래 추적 리스트
token_volumes = defaultdict(float)
buy_transactions = []
sell_transactions = []

# 데이터 분석
for trade in all_data:
    buy = trade["Trade"]["Buy"]
    sell = trade["Trade"]["Sell"]
    transaction_signature = trade["Transaction"]["Signature"]

    # 매수 데이터
    buy_amount = float(buy["Amount"])  # 개수 그대로 사용
    buy_transactions.append({
        "wallet_address": buy["Account"]["Address"],
        "amount": buy_amount,
        "currency_symbol": buy["Currency"]["Symbol"],
        "mint_address": buy["Currency"]["MintAddress"],
        "transaction": transaction_signature
    })

    # 매도 데이터
    sell_amount = float(sell["Amount"])  # 개수 그대로 사용
    sell_transactions.append({
        "wallet_address": sell["Account"]["Address"],
        "amount": sell_amount,
        "currency_symbol": sell["Currency"]["Symbol"],
        "mint_address": sell["Currency"]["MintAddress"],
        "transaction": transaction_signature
    })

    # 토큰별 거래량 누적
    token_volumes[buy["Currency"]["Symbol"]] += buy_amount

# 가장 많이 거래된 토큰 상위 10개 정렬
top_10_tokens = sorted(token_volumes.items(), key=lambda x: x[1], reverse=True)[:10]

# 단일 거래에서 가장 크게 매수/매도한 상위 10개 정렬
top_10_buys = sorted(buy_transactions, key=lambda x: x["amount"], reverse=True)[:10]
top_10_sells = sorted(sell_transactions, key=lambda x: x["amount"], reverse=True)[:10]

# 결과 출력
print("가장 많이 거래된 토큰 TOP 10 (개수 기준):")
for rank, (token, volume) in enumerate(top_10_tokens, start=1):
    print(f"{rank}. {token}: {volume:.6f}")

print("\n단일 거래에서 가장 크게 매수한 TOP 10 (개수 기준):")
for rank, transaction in enumerate(top_10_buys, start=1):
    print(f"{rank}. 지갑 주소: {transaction['wallet_address']}, 매수 금액: {transaction['amount']:.6f} 개, "
          f"토큰: {transaction['currency_symbol']}, 토큰 컨트랙트: {transaction['mint_address']}, 트랜잭션: {transaction['transaction']}")

print("\n단일 거래에서 가장 크게 매도한 TOP 10 (개수 기준):")
for rank, transaction in enumerate(top_10_sells, start=1):
    print(f"{rank}. 지갑 주소: {transaction['wallet_address']}, 매도 금액: {transaction['amount']:.6f} 개, "
          f"토큰: {transaction['currency_symbol']}, 토큰 컨트랙트: {transaction['mint_address']}, 트랜잭션: {transaction['transaction']}")
