from InsightFunctions import *
from optparse import OptionParser

if __name__ == '__main__':
    
    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 2.0.6")
    parser.add_option("-l4", "--l4",
                      action="store_true",
                      dest="L4",
                      default=False,
                      help="L4")
    parser.add_option("-lom", "--lom",
                      action="store_true",
                      dest="LOM",
                      default=False,
                      help="LOM")
    parser.add_option("-hssd", "--hssd",
                      action="store_true",
                      dest="HSSD",
                      default=False,
                      help="HSSD")
    parser.add_option("-mhc", "--mhc",
                      action="store_true",
                      dest="MHC",
                      default=False,
                      help="MHC")
    parser.add_option("-ics", "--ics",
                      action="store_true",
                      dest="ICS",
                      default=False,
                      help="ICS")
    parser.add_option("-goss", "--goss",
                      action="store_true",
                      dest="Goss",
                      default=False,
                      help="Goss")
    (options, args) = parser.parse_args()
    
    if options.L4:
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