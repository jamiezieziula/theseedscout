import random

from prefect import flow
from prefect.blocks.system import JSON


@flow
def generate_donor_id():
    donor_ids = JSON.load("donor-ids").value

    complete = False

    while complete == False:
        donor_id = random.randint(1000, 9999)

        if donor_id in donor_ids:
            continue

        print(donor_id)
        donor_ids.append(donor_id)

        donors = JSON(value=donor_ids)
        donors.save(name="donor-ids", overwrite=True)
        complete = True


if __name__ == "__main__":
    generate_donor_id()
