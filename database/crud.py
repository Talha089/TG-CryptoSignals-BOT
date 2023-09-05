

from datetime import datetime, timedelta

from database.database import session, create_tables
from database.modules import UserPayment

create_tables()


def create_payment_record(full_name: str, chat_id: str, payed_id: str, package_plan: str):
    with session.begin():
        payment = UserPayment(full_name=full_name, chat_id=chat_id, payed_id=payed_id, package_plan=package_plan,
                              paid=True)
        session.add(payment)
    print("new record is created in db")


def get_active_paid_users() -> list:
    check_subscription_expiration()

    with session.begin():
        # Query users whose subscription start date is 3 months or more in the past
        active_paid_users = session.query(UserPayment.chat_id).filter(
            UserPayment.paid == True,
            UserPayment.subscription_expired == False  # Exclude users with expired subscriptions
        ).all()

    return [user.chat_id for user in active_paid_users]


def check_subscription_expiration():
    # Calculated the date of months ago from the current date
    three_months_ago = datetime.now() - timedelta(days=90)
    one_month_ago = datetime.now() - timedelta(days=30)
    six_months_ago = datetime.now() - timedelta(days=180)

    # Query users whose subscription start date is 3 months or more in the past
    three_months_expired_users = session.query(UserPayment).filter(UserPayment.package_plan == "3 months", UserPayment.paid == True,
                                                      UserPayment.subscription_start_date <= three_months_ago).all()

    one_month_expired_users = session.query(UserPayment).filter(UserPayment.package_plan == "1 month", UserPayment.paid == True,
                                                      UserPayment.subscription_start_date <= one_month_ago).all()

    six_months_expired_users = session.query(UserPayment).filter(UserPayment.package_plan == "6 months", UserPayment.paid == True,
                                                      UserPayment.subscription_start_date <= six_months_ago).all()

    # Mark their subscriptions as expired
    for user in three_months_expired_users:
        user.subscription_expired = True

    for user in one_month_expired_users:
        user.subscription_expired = True

    for user in six_months_expired_users:
        user.subscription_expired = True

    # Commit the changes to the database
    session.commit()
    print("check_subscription_expiration func is called")



