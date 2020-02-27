import argparse
import project0

def main(url):
    # Download data
    project0.fetchIncidents(url)

    # Extract Data
    incidents = project0.extractIncidents()

    # Create Dataase
    db = project0.createdb()

    # Insert Data
    project0.dbInsert(db, incidents)

    # Print Status
    project0.dbStatus(db)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="The arrest summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)