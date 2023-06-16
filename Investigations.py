from InsightFunctions import *
from optparse import OptionParser

if __name__ == '__main__':

    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 2.0.6")
    parser.add_option("--lab",
                      action="store_true",
                      dest="Lab",
                      default=False)
    parser.add_option("--lom",
                      action="store_true",
                      dest="LOM",
                      default=False)
    parser.add_option("--hssd",
                      action="store_true",
                      dest="HSSD",
                      default=False)
    parser.add_option("--mhc",
                      action="store_true",
                      dest="MHC",
                      default=False)
    parser.add_option("--ics",
                      action="store_true",
                      dest="ICS",
                      default=False)
    parser.add_option("--goss",
                      action="store_true",
                      dest="Goss",
                      default=False)
    (options, args) = parser.parse_args()
    
    if options.Lab:
        company = "LabFour"
        whenWasTheLastTime(company)
        getInsightInvestigations(company)
        checkForNew(company)
        updateLastTime(company)
    
    if options.LOM:
        company = "Lexus"
        whenWasTheLastTime(company)
        getInsightInvestigations(company)
        checkForNew(company)
        updateLastTime(company)

    if options.HSSD:
        company = "HSSD"
        whenWasTheLastTime(company)
        getInsightInvestigations(company)
        checkForNew(company)
        updateLastTime(company)

    if options.MHC:
        company = "MHC"
        whenWasTheLastTime(company)
        getInsightInvestigations(company)
        checkForNew(company)
        updateLastTime(company)

    if options.ICS:
        company = "ICS"
        whenWasTheLastTime(company)
        getInsightInvestigations(company)
        checkForNew(company)
        updateLastTime(company)

    if options.Goss:
        company = "Gossett"
        whenWasTheLastTime(company)
        getInsightInvestigations(company)
        checkForNew(company)
        updateLastTime(company)