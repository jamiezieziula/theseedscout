import random

from prefect import flow
from prefect.blocks.system import JSON


@flow
def generate_donor_id(
    number_of_ids: int = 1
):
    # Load existing donor IDs
    donor_ids = JSON.load("donor-ids").value

    complete = False

    # Generate Donor ID and ensure it does not already exist
    while complete == False:
        donor_id = random.randint(1000, 9999)

        if donor_id in donor_ids:
            continue

        print(f"The new Donor ID is: {donor_id}")
        donor_ids.append(donor_id)

        donors = JSON(value=donor_ids)
        donors.save(name="donor-ids", overwrite=True)
        complete = True


if __name__ == "__main__":
    generate_donor_id()
