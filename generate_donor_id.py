import random

from prefect import flow
from prefect.blocks.system import JSON
from prefect.blocks.notifications import SlackWebhook


@flow(log_prints=True)
def generate_donor_id(
    number_of_ids: int = 1
):
    # Load existing donor IDs
    donor_ids = JSON.load("donor-ids").value

    new_donor_ids = []

    # Generate Donor ID and ensure it does not already exist
    for i in range(number_of_ids):
        complete = False

        while complete == False:
            donor_id = random.randint(1000, 9999)

            if donor_id in donor_ids:
                continue

            new_donor_ids.append(donor_id)

            complete = True
    
    print(f"The new Donor ID(s) are: {new_donor_ids}")

    # Combined existing and new donor ids
    merged_list = donor_ids + new_donor_ids

    # Send Slack notification
    slack_webhook_block = SlackWebhook.load("new-donor-id-notification")
    slack_webhook_block.notify(f"The new Donor ID(s) are: {new_donor_ids}")

    # Save to JSON block
    donors = JSON(value=merged_list)
    donors.save(name="donor-ids", overwrite=True)


if __name__ == "__main__":
    generate_donor_id()
