# Entry point of the pipeline - for command line trigger or as batch jobs
from loadall_auction_items import main as loadall_auction_items
from populate_transaction_amount import main as populate_transaction_amount
from populate_certificates import main as populate_certificates

def main():
    # Load all auction items
    loadall_auction_items()
    print ('\033[32m', "Completed execution for: %s" % ('Loading all auction items'), '\033[0m', sep='')
    # populate the population, and transaction table
    populate_transaction_amount()
    print ('\033[32m', "Completed execution for: %s" % ('Loading transaction and population data'), '\033[0m', sep='')
    # Populate the certificate table (only if new certificate is found)
    populate_certificates()
    print ('\033[32m', "Completed execution for: %s" % ('Loading certificate data'), '\033[0m', sep='')

if __name__ == '__main__':
    main()
