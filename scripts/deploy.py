from brownie import FundMe, network, MockV3Aggregator, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    print(f"Using account: {account.address}")
    # pass our priceFeed contract address before deployment

    # if we are on rinkeby, pass in rinkeby. If on development server pass in mocks. Otherwise deploy mocks:

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Fundme contract deployed to: {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
