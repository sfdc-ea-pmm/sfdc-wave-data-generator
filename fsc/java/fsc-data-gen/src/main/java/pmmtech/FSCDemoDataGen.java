package pmmtech;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;
import com.opencsv.bean.StatefulBeanToCsv;
import com.opencsv.bean.StatefulBeanToCsvBuilder;
import com.opencsv.exceptions.CsvDataTypeMismatchException;
import com.opencsv.exceptions.CsvRequiredFieldEmptyException;

import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class FSCDemoDataGen {
    private static final String SOURCE_ACCOUNTS_CSV_FILE_PATH = "./SourceAccounts.csv";
    private static final String SOURCE_ZIP_AND_STATES_CSV_FILE_PATH = "./SourceZipCodesAndStates.csv";
    private static final String SOURCE_OPPTY_CSV_FILE_PATH = "./SourceOpportunities.csv";
    private static final String SOURCE_PIPELINE_TRENDING_CSV_FILE_PATH = "./SourcePipelineTrending.csv";
    private static final String GEN_ACCOUNTS_CSV_FILE_PATH = "./FSCAccount.csv";
    private static final String GEN_FIN_ACCOUNTS_CSV_FILE_PATH = "./FSCFinancialAccount.csv";
    private static final String GEN_FIN_ACCOUNT_TRNX_CSV_FILE_PATH = "./FSCFinancialAccountTransaction.csv";
    private static final String GEN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH = "./FSCAccountSnapshot.csv";
    private static final String GEN_FIN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH = "./FSCFinancialAccountSnapshot.csv";
    private static final String GEN_FIN_ACCOUNT_TRN_SNAPSHOT_CSV_FILE_PATH = "./FSCFinancialAccountTransactionSnapshot.csv";
    private static final String GEN_ACTIVITIES_CSV_FILE_PATH = "./FSCActivities.csv";
    private static final String GEN_LEADS_CSV_FILE_PATH = "./FSCLeads.csv";
    private static final String GEN_CASES_CSV_FILE_PATH = "./FSCCases.csv";
    private static final String GEN_CAMPAIGNS_CSV_FILE_PATH = "./FSCCampaigns.csv";
    private static final String GEN_OPPTY_CSV_FILE_PATH = "./FSCOpportunity.csv";
    private static final String GEN_PIPELINE_TRENDING_CSV_FILE_PATH = "./FSCPipelineTrending.csv";    
    private static final String GEN_QUOTA_CSV_FILE_PATH = "./FSCQuota.csv";
    private static final int TOTAL_ACCOUNTS_TO_CREATE = 1000;
    private static final int MIN_ACCOUNTS_TO_CREATE = 7;
    private static final int MAX_ACCOUNTS_TO_CREATE = 15;
    private static final int MAX_FIN_ACCOUNTS_TO_CREATE = 4;
    private static final int MAX_DAYS_BEHIND_REL_START_DATE = 3650; // 10 years in the past
    private static final int MAX_TRANSACTION_AMOUNT = 50000;
    //private static final int MAX_HELD_AWAY_TRANSACTION_AMOUNT = 50000;
    private static final int MIN_TRANSACTION_AMOUNT = 5000;
    private static final int MIN_CONTACT_ANNUAL_INCOME = 50000;
    private static final int MAX_CONTACT_ANNUAL_INCOME = 250000;
    private static final int MAX_LEADS_PER_WEEK = 10;
    private static final int MIN_NUMBER_SENT_PER_CAMPAIGN = 20;
    private static final int MAX_NUMBER_SENT_PER_CAMPAIGN = 100;

    public static void main(String[] args)
            throws IOException, ParseException, CsvDataTypeMismatchException, CsvRequiredFieldEmptyException
    {
        try (
            Reader srcAcctReader = Files.newBufferedReader(Paths.get(SOURCE_ACCOUNTS_CSV_FILE_PATH));
            Reader srcZipStatesReader = Files.newBufferedReader(Paths.get(SOURCE_ZIP_AND_STATES_CSV_FILE_PATH));
            Reader srcOpptyReader = Files.newBufferedReader(Paths.get(SOURCE_OPPTY_CSV_FILE_PATH));
            Reader srcPipeTrendReader = Files.newBufferedReader(Paths.get(SOURCE_PIPELINE_TRENDING_CSV_FILE_PATH));
            Writer genAcctWriter = Files.newBufferedWriter(Paths.get(GEN_ACCOUNTS_CSV_FILE_PATH));
            Writer genFinAcctWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNTS_CSV_FILE_PATH));
            Writer genFinAcctTrnWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNT_TRNX_CSV_FILE_PATH));
            Writer genActivityWriter = Files.newBufferedWriter(Paths.get(GEN_ACTIVITIES_CSV_FILE_PATH));
            Writer genCaseWriter = Files.newBufferedWriter(Paths.get(GEN_CASES_CSV_FILE_PATH));
            Writer genLeadWriter = Files.newBufferedWriter(Paths.get(GEN_LEADS_CSV_FILE_PATH));
            Writer genCampWriter = Files.newBufferedWriter(Paths.get(GEN_CAMPAIGNS_CSV_FILE_PATH));
            Writer genOpptyWriter = Files.newBufferedWriter(Paths.get(GEN_OPPTY_CSV_FILE_PATH));
            Writer genPipeTrendWriter = Files.newBufferedWriter(Paths.get(GEN_PIPELINE_TRENDING_CSV_FILE_PATH));
            Writer genQuotaWriter = Files.newBufferedWriter(Paths.get(GEN_QUOTA_CSV_FILE_PATH));
            Writer genAcctSnapWriter = Files.newBufferedWriter(Paths.get(GEN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH)); 
            Writer genFinAcctSnapWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH)); 
            Writer genFinAcctTrnSnapWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNT_TRN_SNAPSHOT_CSV_FILE_PATH));
            
            CSVWriter genAcctSnapCsvWriter = new CSVWriter(genAcctSnapWriter,
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.NO_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END);
                
            CSVWriter genFinAcctSnapCsvWriter = new CSVWriter(genFinAcctSnapWriter,
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.NO_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END);

            CSVWriter genFinAcctTrnSnapCsvWriter = new CSVWriter(genFinAcctTrnSnapWriter,
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.NO_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END);
        ){
            CsvToBean<AccountCsv> acctCsvToBean = new CsvToBeanBuilder<AccountCsv>(srcAcctReader)
                    .withType(AccountCsv.class)
                    .withIgnoreLeadingWhiteSpace(true)
                    .build();

            CsvToBean<ZipAndStateCsv> zipAndStatesCsvToBean = new CsvToBeanBuilder<ZipAndStateCsv>(srcZipStatesReader)
                .withType(ZipAndStateCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<OpportunityCsv> opptyCsvToBean = new CsvToBeanBuilder<OpportunityCsv>(srcOpptyReader)
                .withType(OpportunityCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<PipelineTrendingCsv> pipeTrendCsvToBean = new CsvToBeanBuilder<PipelineTrendingCsv>(srcPipeTrendReader)
                .withType(PipelineTrendingCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            StatefulBeanToCsv<AccountCsv> genAcctBeanToCsv = new StatefulBeanToCsvBuilder<AccountCsv>(genAcctWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<FinancialAccountCsv> genFinAcctBeanToCsv = new StatefulBeanToCsvBuilder<FinancialAccountCsv>(genFinAcctWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<FinancialAccountTransactionCsv> genFinAcctTrnBeanToCsv = new StatefulBeanToCsvBuilder<FinancialAccountTransactionCsv>(genFinAcctTrnWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();
                
            StatefulBeanToCsv<ActivityCsv> genActivityBeanToCsv = new StatefulBeanToCsvBuilder<ActivityCsv>(genActivityWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<CaseCsv> genCaseBeanToCsv = new StatefulBeanToCsvBuilder<CaseCsv>(genCaseWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<LeadCsv> genLeadBeanToCsv = new StatefulBeanToCsvBuilder<LeadCsv>(genLeadWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<CampaignCsv> genCampBeanToCsv = new StatefulBeanToCsvBuilder<CampaignCsv>(genCampWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<OpportunityCsv> genOpptyBeanToCsv = new StatefulBeanToCsvBuilder<OpportunityCsv>(genOpptyWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<PipelineTrendingCsv> genPipeTrendBeanToCsv = new StatefulBeanToCsvBuilder<PipelineTrendingCsv>(genPipeTrendWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<QuotaCsv> genQuotaBeanToCsv = new StatefulBeanToCsvBuilder<QuotaCsv>(genQuotaWriter)
                .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER)
                .build();
            
            String[] snapshotDatesHeader = new String[] {
                "SnapshotDate",
                "SnapshotTextDate"
            };
            genAcctSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDatesHeader, AccountCsv.getCsvHeader()));
            genFinAcctSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDatesHeader, FinancialAccountCsv.getCsvHeader()));
            genFinAcctTrnSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDatesHeader, FinancialAccountTransactionCsv.getCsvHeader()));
            
            Iterator<AccountCsv> csvAccountIterator = acctCsvToBean.iterator();
            Iterator<ZipAndStateCsv> csvZipAndStatesIterator = zipAndStatesCsvToBean.iterator();
            Map<String, List<String>> zipAndStatesTable = new HashMap<String, List<String>>();
            List<ZipAndStateCsv> lstCitiesAndState = new LinkedList<ZipAndStateCsv>();
            List<AccountCsv> lstAccounts = new LinkedList<AccountCsv>();
            List<FinancialAccountCsv> lstFinAccounts = new LinkedList<FinancialAccountCsv>();
            List<FinancialAccountTransactionCsv> lstFinAccountTransactions = new LinkedList<FinancialAccountTransactionCsv>();
            List<ActivityCsv> lstActivities = new LinkedList<ActivityCsv>();
            List<CaseCsv> lstCases = new LinkedList<CaseCsv>();
            List<LeadCsv> lstLeads = new LinkedList<LeadCsv>();
            List<CampaignCsv> lstCampaigns = new LinkedList<CampaignCsv>();
            Random randHelper = new Random();
            int accountsCreatedCount = 0;
            int accountsToCreateCount = 0;
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
            Calendar todayDate = Calendar.getInstance();
            Calendar currentSnapshotDate = Calendar.getInstance();
            currentSnapshotDate.add(Calendar.YEAR, -2); // 2 years to the past
            int weeksCounter = 0;

            // Account Record Type based on probability
            LinkedList<AccountRecordType> lstRecordTypes = new LinkedList<AccountRecordType>();
            AccountRecordType aRt;
            
            // Individual Record Type
            aRt = new AccountRecordType();
            aRt.setRelativeProbability(1);
            aRt.setRecordTypeName("Individual");
            lstRecordTypes.add(aRt);

            // Household Record Type
            aRt = new AccountRecordType();
            aRt.setRelativeProbability(1);
            aRt.setRecordTypeName("Household");
            lstRecordTypes.add(aRt);

            // Person Account Record Type
            aRt = new AccountRecordType();
            aRt.setRelativeProbability(2);
            aRt.setRecordTypeName("Person Account");
            lstRecordTypes.add(aRt);

            RandomAccountRecordTypeSelector rndAcctRecTypeSel = new RandomAccountRecordTypeSelector(lstRecordTypes);

            // Financial Account Record Type based on probability
            LinkedList<FinancialAccountRecordType> lstFinAccRecordTypes = new LinkedList<FinancialAccountRecordType>();
            FinancialAccountRecordType finAccRt;
            
            // Bank Account Record Type
            finAccRt = new FinancialAccountRecordType();
            finAccRt.setRelativeProbability(10);
            finAccRt.setRecordTypeName("Bank Account");
            lstFinAccRecordTypes.add(finAccRt);

            // Investment Account Record Type
            finAccRt = new FinancialAccountRecordType();
            finAccRt.setRelativeProbability(85);
            finAccRt.setRecordTypeName("Investment Account");
            lstFinAccRecordTypes.add(finAccRt);

            // Credit Card Record Type
            finAccRt = new FinancialAccountRecordType();
            finAccRt.setRelativeProbability(3);
            finAccRt.setRecordTypeName("Credit Card");
            lstFinAccRecordTypes.add(finAccRt);

            // Savings Account Record Type
            finAccRt = new FinancialAccountRecordType();
            finAccRt.setRelativeProbability(15);
            finAccRt.setRecordTypeName("Savings Account");
            lstFinAccRecordTypes.add(finAccRt);

            RandomFinancialAccountRecordTypeSelector rndFinAcctRecTypeSel = new RandomFinancialAccountRecordTypeSelector(lstFinAccRecordTypes);

            // Billing State based on probability
            LinkedList<BillingState> lstBillingStates = new LinkedList<BillingState>();
            BillingState billState = new BillingState();
            billState.setRelativeProbability(5);
            billState.setState("CA");
            lstBillingStates.add(billState);

            billState = new BillingState();
            billState.setRelativeProbability(4);
            billState.setState("NY");
            lstBillingStates.add(billState);

            billState = new BillingState();
            billState.setRelativeProbability(3);
            billState.setState("NJ");
            lstBillingStates.add(billState);

            billState = new BillingState();
            billState.setRelativeProbability(3);
            billState.setState("FL");
            lstBillingStates.add(billState);

            billState = new BillingState();
            billState.setRelativeProbability(2);
            billState.setState("TX");
            lstBillingStates.add(billState);

            billState = new BillingState();
            billState.setRelativeProbability(2);
            billState.setState("IL");
            lstBillingStates.add(billState);

            billState = new BillingState();
            billState.setRelativeProbability(2);
            billState.setState("PA");
            lstBillingStates.add(billState);

            billState = new BillingState();
            billState.setRelativeProbability(2);
            billState.setState("MI");
            lstBillingStates.add(billState);

            RandomBillingStateSelector rndBillStateSel = new RandomBillingStateSelector(lstBillingStates);

            // Random Held Away based on probability
            LinkedList<HeldAwayItem> lstHeldAwayItems = new LinkedList<HeldAwayItem>();
            HeldAwayItem heldAwayItem = new HeldAwayItem();
            heldAwayItem.setHeldAway(true);
            heldAwayItem.setRelativeProbability(1);
            lstHeldAwayItems.add(heldAwayItem);
            heldAwayItem = new HeldAwayItem();
            heldAwayItem.setHeldAway(false);
            heldAwayItem.setRelativeProbability(3);
            lstHeldAwayItems.add(heldAwayItem);
            RandomHeldAwaySelector rndHeldAway = new RandomHeldAwaySelector(lstHeldAwayItems);

            // Marketing Segments
            ArrayList<String> lstMarketingSegments = new ArrayList<String>();
            Collections.addAll(lstMarketingSegments, "Mass Affluent", "High Net Worth", "Female Investor", "Millennial");

            // Investment Objectives
            ArrayList<String> lstInvestmentObjectives = new ArrayList<String>();
            Collections.addAll(lstInvestmentObjectives, "Conservative Income", "Income", "Balanced", "Growth", "Aggressive Growth");

            // Investment Objectives
            ArrayList<String> lstInvestmentExperience = new ArrayList<String>();
            Collections.addAll(lstInvestmentExperience, "Experienced", "Moderately Experienced", "Moderately Inexperienced", "Inexperienced");

            // Client Category
            ArrayList<String> lstClientCats = new ArrayList<String>();
            Collections.addAll(lstClientCats, "Platinum", "Gold", "Silver", "Bronze");

            // Gender
            ArrayList<String> lstGenders = new ArrayList<String>();
            Collections.addAll(lstGenders, "Male", "Female");            

            // Activity Types
            ArrayList<String> lstActivityTypes = new ArrayList<String>();
            Collections.addAll(lstActivityTypes, 
                "Call", 
                "Meeting",
                "Email",
                "Other"
            );
            
            // Lead Status
            ArrayList<String> lstLeadStatus = new ArrayList<String>();
            Collections.addAll(lstLeadStatus, 
                "Closed - Converted", 
                "Closed - Not Converted",
                "New - Not Contacted",
                "Nurturing - Contacted",
                "Working - Contacted"
            );

            // Zips and State, States & Cities
            while (csvZipAndStatesIterator.hasNext()) {
                ZipAndStateCsv currCsvBillSt = csvZipAndStatesIterator.next();
                lstCitiesAndState.add(currCsvBillSt);
                List<String> zipListByState;
                String currState = currCsvBillSt.getState();
                
                if (zipAndStatesTable.containsKey(currState)) {
                    zipListByState = (List<String>)zipAndStatesTable.get(currState);
                } 
                else {
                    zipListByState = new LinkedList<String>();
                    zipAndStatesTable.put(currState, zipListByState);
                }

                zipListByState.add(currCsvBillSt.getZipCode());
            }
            /*
            // We are gonna generate data for each week from one year in the past until today
            int cantIterations = 0;
            while (currentSnapshotDate.compareTo(todayDate) <= 0) {

                weeksCounter++;
                
                if(lstAccounts.size() > 0){
                    // First of all, tweak the existing business. We are gonna change some existing accounts
                    int cantItemsToChange = Helper.getRandomNumberInRange(0, lstAccounts.size());
                    List<Integer> lstAcctIndexesToChange = Helper.getRandomIndexesList(lstAccounts.size(), cantItemsToChange);
                    
                    for (Integer index : lstAcctIndexesToChange) {
                        
                        AccountCsv acctToChange = lstAccounts.get(index);
                        
                        // Rollup numbers for each account:
                        double totalFinAcctsPrimaryOwner = acctToChange.getTotalFinAcctsPrimaryOwner();
                        // @TODO: double totalFinAcctsJointOwner;

                        double totalAUMPrimaryOwner = acctToChange.getTotalAUMPrimaryOwner();
                        // @TODO: double totalAUMJointOwner;

                        double totalHeldFinAcctsPrimaryOwner = acctToChange.getTotalHeldFinAcctsPrimaryOwner();
                        // @TODO: double totalHeldFinAcctsJointOwner;
                        
                        for (FinancialAccountCsv finAcctToChange : acctToChange.getFinancialAccounts()) {
                            double balance = finAcctToChange.getBalance();
                            
                            if (!finAcctToChange.isHeldAway() || (finAcctToChange.isHeldAway() && weeksCounter == 4)) {
                                // Random Updates to held away accounts occur once a month
                                // We add a new transaction to the account
                                FinancialAccountTransactionCsv t = new FinancialAccountTransactionCsv();
                                t.setId("Trnx-" + finAcctToChange.getTransactions().size() + "-" + finAcctToChange.getId());
                                t.setAccountData(acctToChange);
                                t.setFinancialAccountId(finAcctToChange.getId());
                                t.setOwnerName(acctToChange.getOwnerName());
                                
                                Double dblBalance = Double.valueOf(balance);
                                int rndDirection = Helper.getRandomNumberInRange(-1, 1);
                                int trnxAmount = 0;

                                // Handle the account's held away trending
                                if (!acctToChange.getHeldAwayWillIncrease() && finAcctToChange.isHeldAway() && weeksCounter == 4) {
                                    // The held away is set to decrease
                                    rndDirection = -1;
                                }

                                if (rndDirection < 0 && dblBalance.intValue() > 1) {
                                    t.setTransactionType("Debit");                                    
                                    trnxAmount = Helper.getRandomNumberInRange(1, dblBalance.intValue());
                                } 
                                else {
                                    t.setTransactionType("Credit");
                                    trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT, MAX_TRANSACTION_AMOUNT);
                                }

                                // Transaction Date now() down to 6 days before
                                int trnxDaysBefore = Helper.getRandomNumberInRange(1, 6);
                                Calendar calTrnxDate = (Calendar)currentSnapshotDate.clone();
                                calTrnxDate.add(Calendar.DAY_OF_MONTH, -trnxDaysBefore);
                                t.setTransactionDate(dateFormat.format(calTrnxDate.getTime()));
                                
                                // Transaction Amount
                                t.setAmount(trnxAmount);

                                double arithmeticAmount = t.getArithmeticAmount();
                                double financialAccountBalance = balance + arithmeticAmount;
                                lstFinAccountTransactions.add(t);
                                finAcctToChange.getTransactions().add(t);
                                finAcctToChange.setBalance(financialAccountBalance);

                                // Held away management of financial account
                                if (finAcctToChange.isHeldAway()) {
                                    totalHeldFinAcctsPrimaryOwner += arithmeticAmount;
                                } 
                                else {
                                    totalAUMPrimaryOwner += arithmeticAmount;                                    
                                }

                                totalFinAcctsPrimaryOwner += arithmeticAmount;
                            }
                        }

                        acctToChange.setTotalFinAcctsPrimaryOwner(totalFinAcctsPrimaryOwner);
                        acctToChange.setTotalAUMPrimaryOwner(totalAUMPrimaryOwner);
                        acctToChange.setTotalHeldFinAcctsPrimaryOwner(totalHeldFinAcctsPrimaryOwner);

                        // Add some activities to the account
                        int cntActivitiesToAdd = Helper.getRandomNumberInRange(1, 3);
                        for (int a = 0; a < cntActivitiesToAdd; a++) {
                            ActivityCsv actToCreate = new ActivityCsv();
                            String rndActivityType = lstActivityTypes.get(Helper.getRandomNumberInRange(0, lstActivityTypes.size() - 1));
                            int activityDaysBefore = Helper.getRandomNumberInRange(1, 6);
                            Calendar calActivityDate = (Calendar)currentSnapshotDate.clone();
                            calActivityDate.add(Calendar.DAY_OF_MONTH, -activityDaysBefore);
                            
                            actToCreate.setAccountId(acctToChange.getId());
                            actToCreate.setId("Activity-" + acctToChange.getActivities().size() + "-" + acctToChange.getId());
                            actToCreate.setAccountName(acctToChange.getName());
                            actToCreate.setAccountRecordTypeName(acctToChange.getRecordTypeName());
                            actToCreate.setActivityDate(dateFormat.format(calActivityDate.getTime()));
                            actToCreate.setType(rndActivityType);
                            lstActivities.add(actToCreate);
                            acctToChange.getActivities().add(actToCreate);
                        }

                        // Add some cases to the account
                        int cntCasesToAdd = Helper.getRandomNumberInRange(0, 2);
                        for (int c = 0; c < cntCasesToAdd; c++) {
                            CaseCsv caseToCreate = new CaseCsv();
                            int caseDaysBefore = Helper.getRandomNumberInRange(1, 6);
                            Calendar calCaseDate = (Calendar)currentSnapshotDate.clone();
                            calCaseDate.add(Calendar.DAY_OF_MONTH, -caseDaysBefore);
                            
                            caseToCreate.setAccountData(acctToChange);
                            caseToCreate.setId("Case-" + acctToChange.getCases().size() + "-" + acctToChange.getId());
                            caseToCreate.setCreatedDate(dateFormat.format(calCaseDate.getTime()));
                            lstCases.add(caseToCreate);
                            acctToChange.getCases().add(caseToCreate);
                        }
                    }

                    System.out.println("Modified: " + cantItemsToChange + " accounts.");
                }
                

                // NEW ACCOUNTS (CLIENTS)
                // How many accounts are we gonna add?
                accountsToCreateCount = Helper.getRandomNumberInRange(MIN_ACCOUNTS_TO_CREATE, MAX_ACCOUNTS_TO_CREATE);
                
                // This is to avoid running out of accounts in the source CSV
                if (accountsCreatedCount + accountsToCreateCount > TOTAL_ACCOUNTS_TO_CREATE) {
                    accountsToCreateCount = TOTAL_ACCOUNTS_TO_CREATE - accountsCreatedCount;
                }
                
                for (int i = 0; i < accountsToCreateCount; i++) {
                    AccountCsv sourceCsvAccount = csvAccountIterator.next();
                    AccountCsv demoAccount = new AccountCsv();
                    int daysForRelStartDate = Helper.getRandomNumberInRange(0, MAX_DAYS_BEHIND_REL_START_DATE);
                    Calendar calRelStartDate = (Calendar)currentSnapshotDate.clone();
                    calRelStartDate.add(Calendar.DAY_OF_MONTH, -daysForRelStartDate);
                    Date dtRelStartDate = calRelStartDate.getTime();
                    
                    demoAccount.setAccountNumber(sourceCsvAccount.getAccountNumber());
                    demoAccount.setId(sourceCsvAccount.getId());
                    demoAccount.setInvestmentExperience(sourceCsvAccount.getInvestmentExperience());
                    demoAccount.setInvestmentObjectives(sourceCsvAccount.getInvestmentObjectives());
                    demoAccount.setName(sourceCsvAccount.getName());
                    demoAccount.setRecordTypeName(rndAcctRecTypeSel.getRandomAccountRecordType().getRecordTypeName());
                    demoAccount.setRelationshipStartDate(dateFormat.format(dtRelStartDate));
                    demoAccount.setYearsSinceClient(Helper.getDiffYears(dtRelStartDate, currentSnapshotDate.getTime()));
                    demoAccount.setOwnerName("Demo Financial Advisor");
                    
                    String currMarkSeg = lstMarketingSegments.get(Helper.getRandomNumberInRange(0, lstMarketingSegments.size() - 1));
                    demoAccount.setMarketingSegment(currMarkSeg);
                    
                    String currInvObj = lstInvestmentObjectives.get(Helper.getRandomNumberInRange(0, lstInvestmentObjectives.size() - 1));
                    demoAccount.setInvestmentObjectives(currInvObj);

                    String currInvExp = lstInvestmentExperience.get(Helper.getRandomNumberInRange(0, lstInvestmentExperience.size() - 1));
                    demoAccount.setInvestmentExperience(currInvExp);

                    // Tier 1, Tier 2 or Tier 3
                    demoAccount.setServiceModel("Tier " + Helper.getRandomNumberInRange(1, 3));

                    String rndClientCat = lstClientCats.get(Helper.getRandomNumberInRange(0, lstClientCats.size() - 1));
                    demoAccount.setClientCategory(rndClientCat);

                    // Fake phone
                    int phonePart1 = Helper.getRandomNumberInRange(221, 555);
                    int phonePart2 = Helper.getRandomNumberInRange(100, 999);
                    int phonePart3 = Helper.getRandomNumberInRange(1000, 9999);
                    demoAccount.setPhone(phonePart1 + "-" + phonePart2 + "-" + phonePart3);

                    demoAccount.setPrimaryContactAge(Helper.getRandomNumberInRange(17, 75));
                    demoAccount.setPrimaryContactAnnualIncome(Helper.getRandomNumberInRange(MIN_CONTACT_ANNUAL_INCOME, MAX_CONTACT_ANNUAL_INCOME));
                    demoAccount.setPrimaryContactEmail("user-" + sourceCsvAccount.getAccountNumber() + "@fsc-demo.com");
                    if (demoAccount.getMarketingSegment().equalsIgnoreCase("Female Investor")) {
                        demoAccount.setPrimaryContactGender("Female");
                    } 
                    else {
                        String rndGender = lstGenders.get(randHelper.nextInt(2));
                        demoAccount.setPrimaryContactGender(rndGender);
                    }
                    
                    String rndBillingState = rndBillStateSel.getRandomBillingState().getState();
                    demoAccount.setBillingState(rndBillingState);
                    List<String> zipListByState = (List<String>)zipAndStatesTable.get(rndBillingState);
                    String rndPostalCode = zipListByState.get(Helper.getRandomNumberInRange(0, zipListByState.size() - 1));
                    demoAccount.setBillingPostalCode(rndPostalCode);

                    // FinServ__LastReview__c (Random date between today and -1 month)
		            // FinServ__LastInteraction__c (Random date between today and FinServ__LastReview__c)
                    // FinServ__NextReview__c (Today() + Random days 1, 30)
                    
                    int daysSinceLastReview = Helper.getRandomNumberInRange(1, 30);
                    int daysSinceLastInteraction = Helper.getRandomNumberInRange(0, daysSinceLastReview);
                    int daysUntilNextReview = Helper.getRandomNumberInRange(15, 30);

                    Calendar calLastReviewDate = (Calendar)currentSnapshotDate.clone();
                    Calendar calLastInteractionDate = (Calendar)currentSnapshotDate.clone();
                    Calendar calNextReviewDate = (Calendar)currentSnapshotDate.clone();

                    calLastReviewDate.add(Calendar.DAY_OF_MONTH, -daysSinceLastReview);
                    calLastInteractionDate.add(Calendar.DAY_OF_MONTH, -daysSinceLastInteraction);
                    calNextReviewDate.add(Calendar.DAY_OF_MONTH, daysUntilNextReview);
                    
                    demoAccount.setLastReview(dateFormat.format(calLastReviewDate.getTime()));
                    demoAccount.setLastInteraction(dateFormat.format(calLastInteractionDate.getTime()));
                    demoAccount.setNextReview(dateFormat.format(calNextReviewDate.getTime()));

                    // What are we gonna do with held away? Which will be the trending?
                    int rndHeldAwayTrending = Helper.getRandomNumberInRange(0, 1);
                    demoAccount.setHeldAwayWillIncrease(rndHeldAwayTrending == 1);

                    lstAccounts.add(demoAccount);

                    // Rollup numbers for each account:
                    double totalAUMPrimaryOwner = 0;
                    // @TODO: double totalAUMJointOwner;
                    
                    double totalFinAcctsPrimaryOwner = 0;
                    // @TODO: double totalFinAcctsJointOwner;

                    double totalHeldFinAcctsPrimaryOwner = 0;
                    // @TODO: double totalHeldFinAcctsJointOwner;
                    
                    double totalNumberOfFinAccountsPrimaryOwner = 0;                    
                    
                    // FINANCIAL ACCOUNTS

                    int finAccToCreateCount = Helper.getRandomNumberInRange(1, MAX_FIN_ACCOUNTS_TO_CREATE);
                    
                    for (int j = 0; j < finAccToCreateCount; j++) {
                        FinancialAccountCsv finAcct = new FinancialAccountCsv();
                        finAcct.setId("FinAcct-" + demoAccount.getId() + "-" + j);
                        finAcct.setAccountData(demoAccount);
                        finAcct.setOwnerName(demoAccount.getOwnerName());                        
                        
                        String rndFinAcctRecType = rndFinAcctRecTypeSel.getRandomFinancialAccountRecordType().getRecordTypeName();
                        finAcct.setRecordTypeName(rndFinAcctRecType);

                        // Financial Account Types
                        ArrayList<String> lstFinAccountTypes = new ArrayList<String>();                        
                                               
                        switch (rndFinAcctRecType) {
                            case "Investment Account":
                                Collections.addAll(lstFinAccountTypes, 
                                    "Brokerage",                                    
                                    "Mutual Fund",
                                    "Fixed Annuity",
                                    "Managed Account"
                                );
                                break;

                            case  "Credit Card":
                                finAcct.setFinancialAccountType("Credit Card");
                                break;

                            case "Bank Account":
                                Collections.addAll(lstFinAccountTypes, 
                                    "Cash Management Account", 
                                    "Checking"
                                );
                                break;
                            
                            case "Savings Account":
                                finAcct.setFinancialAccountType("Savings");
                                break;
                        }

                        if (finAcct.getFinancialAccountType() == null || finAcct.getFinancialAccountType().equals("")) {
                            String rndFinAcctType = lstFinAccountTypes.get(Helper.getRandomNumberInRange(0, lstFinAccountTypes.size() - 1));
                            finAcct.setFinancialAccountType(rndFinAcctType);
                        }

                        finAcct.setHeldAway(rndHeldAway.getRandomHeldAwayItem().getHeldAway());
                        double financialAccountBalance = 0;
                        // @TODO: JointOwner

                        // Financial Account Transactions
                        int trxToCreateCount = Helper.getRandomNumberInRange(1, 5);
                        
                        for (int k = 0; k < trxToCreateCount; k++) {
                            FinancialAccountTransactionCsv transaction = new FinancialAccountTransactionCsv();
                            transaction.setId("Trnx-" + k + "-" + finAcct.getId());
                            transaction.setAccountData(demoAccount);
                            transaction.setFinancialAccountId(finAcct.getId());
                            transaction.setOwnerName(demoAccount.getOwnerName());
                            
                            // Transaction Type, now are all credits
                            transaction.setTransactionType("Credit");

                            // Transaction Date now() down to 6 days before
                            int trnxDaysBefore = Helper.getRandomNumberInRange(1, 6);
                            Calendar calTrnxDate = (Calendar)currentSnapshotDate.clone();
                            calTrnxDate.add(Calendar.DAY_OF_MONTH, -trnxDaysBefore);
                            transaction.setTransactionDate(dateFormat.format(calTrnxDate.getTime()));
                            
                            // Transaction Amount
                            int trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT, MAX_TRANSACTION_AMOUNT);
                            transaction.setAmount(trnxAmount);

                            financialAccountBalance += transaction.getArithmeticAmount();
                            lstFinAccountTransactions.add(transaction);
                            finAcct.getTransactions().add(transaction);
                        }

                        finAcct.setBalance(financialAccountBalance);
                        lstFinAccounts.add(finAcct);
                        demoAccount.getFinancialAccounts().add(finAcct);
                        
                        // Management of financial account
                        if (finAcct.isHeldAway()) {
                            // Held Away
                            totalHeldFinAcctsPrimaryOwner += financialAccountBalance;
                        } 
                        else {
                            // Asset Under Management
                            totalAUMPrimaryOwner += financialAccountBalance;                            
                        }

                        totalFinAcctsPrimaryOwner += financialAccountBalance;
                        totalNumberOfFinAccountsPrimaryOwner++;
                    }

                    // Assets Under Management (AUM) as Primary Owner
                    demoAccount.setTotalAUMPrimaryOwner(totalAUMPrimaryOwner);
                    demoAccount.setTotalFinAcctsPrimaryOwner(totalFinAcctsPrimaryOwner);
                    demoAccount.setTotalHeldFinAcctsPrimaryOwner(totalHeldFinAcctsPrimaryOwner);
                    demoAccount.setTotalNumberOfFinAccountsPrimaryOwner(totalNumberOfFinAccountsPrimaryOwner);
                }

                String snapshotTextDate = dateFormat.format(currentSnapshotDate.getTime());
                String[] snapshotDates = new String[] {
                    snapshotTextDate,
                    snapshotTextDate
                };                
                
                // Record Snapshots
                for (AccountCsv acctForSnapshot : lstAccounts) {
                    genAcctSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDates, acctForSnapshot.getRowOfData()));
                }

                for (FinancialAccountCsv finAcctForSnapshot : lstFinAccounts) {
                    genFinAcctSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDates, finAcctForSnapshot.getRowOfData()));
                }

                for (FinancialAccountTransactionCsv trForSnapshot : lstFinAccountTransactions) {
                    genFinAcctTrnSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDates, trForSnapshot.getRowOfData()));
                }
            
                cantIterations++; // One more week/iterarion
                currentSnapshotDate.add(Calendar.WEEK_OF_YEAR, 1); // Step one week to the future
                accountsCreatedCount += accountsToCreateCount;

                if (weeksCounter == 4) {
                    weeksCounter = 0;

                    // Campaings, one per month
                    CampaignCsv camp = new CampaignCsv();
                    camp.setStartDate(dateFormat.format(currentSnapshotDate.getTime()));
                    int campNumberSent = Helper.getRandomNumberInRange(MIN_NUMBER_SENT_PER_CAMPAIGN, MAX_NUMBER_SENT_PER_CAMPAIGN);
                    int campNumberOfResp = Helper.getRandomNumberInRange(0, campNumberSent);
                    camp.setNumberSent(campNumberSent);
                    camp.setNumberOfResponses(campNumberOfResp);
                    camp.setId("Campaign-" + (lstCampaigns.size() + 1));
                    lstCampaigns.add(camp);
                }

                System.out.println("Created: " + accountsToCreateCount + " accounts."); 
                
                // Leads
                int cntLeads = Helper.getRandomNumberInRange(0, MAX_LEADS_PER_WEEK);
                for (int l = 0; l < cntLeads; l++) {
                    LeadCsv lead = new LeadCsv();
                    int leadDaysBefore = Helper.getRandomNumberInRange(1, 6);
                    Calendar calLeadDate = (Calendar)currentSnapshotDate.clone();
                    calLeadDate.add(Calendar.DAY_OF_MONTH, -leadDaysBefore);
                    lead.setCreatedDate(dateFormat.format(calLeadDate.getTime()));
                    String rndLeadStatus = lstLeadStatus.get(Helper.getRandomNumberInRange(0, lstLeadStatus.size() - 1));
                    lead.setStatus(rndLeadStatus);
                    lead.setId("Lead-" + (lstLeads.size() + 1));
                    lstLeads.add(lead);
                }
            }

            genAcctBeanToCsv.write(lstAccounts);
            genFinAcctBeanToCsv.write(lstFinAccounts);
            genFinAcctTrnBeanToCsv.write(lstFinAccountTransactions);
            genActivityBeanToCsv.write(lstActivities);
            genCaseBeanToCsv.write(lstCases);
            genLeadBeanToCsv.write(lstLeads);
            genCampBeanToCsv.write(lstCampaigns);

            System.out.println("Count of weeks: " + cantIterations);
            System.out.println("Total created clients: " + accountsCreatedCount);*/

            // SECOND PART: Opportunity, Pipeline Trending and Quota data            
            Iterator<OpportunityCsv> csvOpptyIterator = opptyCsvToBean.iterator();
            Iterator<PipelineTrendingCsv> csvPipeTrendIterator = pipeTrendCsvToBean.iterator();
            Map<String, OpportunityCsv> opptyMap = new HashMap<String, OpportunityCsv>();
            Map<String, AccountCsv> accountMap = new HashMap<String, AccountCsv>();
            Map<String, UserOwnerCsv> opptyOwnersMap = new HashMap<String, UserOwnerCsv>();
            List<QuotaCsv> lstQuota = new LinkedList<QuotaCsv>();
            List<PipelineTrendingCsv> lstPipelineTrending = new LinkedList<PipelineTrendingCsv>();
            UserOwnerCsv currOpptyOwner;
            AccountCsv currAccount;
            int activityIndex = 1;
            
            // First we iterate on opportunities
            while (csvOpptyIterator.hasNext()) {
                OpportunityCsv currentOppty = csvOpptyIterator.next();
                String opptyId = currentOppty.getId();
                String accountId = currentOppty.getAccountId();
                String opptyOwnerId = currentOppty.getOwnerId();

                // Owner exists?
                if (!opptyOwnersMap.containsKey(opptyOwnerId)) {
                    currOpptyOwner = new UserOwnerCsv();
                    currOpptyOwner.setId(opptyOwnerId);
                    currOpptyOwner.setName(currentOppty.getOpportunityOwner());
                    currOpptyOwner.setSmallPhotoUrl("");
                    ZipAndStateCsv rndGeoInfo = lstCitiesAndState.get(Helper.getRandomNumberInRange(0, lstCitiesAndState.size() - 1));
                    currOpptyOwner.setState(rndGeoInfo.getState());
                    currOpptyOwner.setCity(rndGeoInfo.getCity());

                    opptyOwnersMap.put(opptyOwnerId, currOpptyOwner);
                }
                else {
                    currOpptyOwner = opptyOwnersMap.get(opptyOwnerId);
                }

                // Account exists?
                if (!accountMap.containsKey(accountId)) {
                    currAccount = new AccountCsv();
                    currAccount.setId(accountId);
                    currAccount.setName(currentOppty.getAccountName());
                    
                    String rndMarkSeg = lstMarketingSegments.get(Helper.getRandomNumberInRange(0, lstMarketingSegments.size() - 1));
                    String rndClientCat = lstClientCats.get(Helper.getRandomNumberInRange(0, lstClientCats.size() - 1));
                    
                    currAccount.setMarketingSegment(rndMarkSeg);
                    currAccount.setClientCategory(rndClientCat);
                    currAccount.setIndustry(currentOppty.getAccountIndustry());
                    accountMap.put(accountId, currAccount);
                }
                else {
                    currAccount = accountMap.get(accountId);
                }

                currentOppty.setAccountData(currAccount);
                currentOppty.setOwnerData(currOpptyOwner);
                currentOppty.setActivityId("Activity " + activityIndex);

                opptyMap.put(opptyId, currentOppty);

                activityIndex++;
            }

            // Quota file, data for each owner, 3 years quota
            
            for (UserOwnerCsv oppOwner : opptyOwnersMap.values()) {
                
                Calendar quotaStartDate = Calendar.getInstance();
                quotaStartDate.add(Calendar.YEAR, -2); // 2 years to the past
                int currentYear = quotaStartDate.get(Calendar.YEAR);                

                for (int yearStep = 0; yearStep <= 2; yearStep++) {
                
                    for (int monthStep = 1; monthStep <= 12; monthStep++) {
                        
                        QuotaCsv quotaItem = new QuotaCsv();
                        quotaItem.setUserOwnerData(oppOwner);
                        quotaStartDate.set(currentYear, monthStep - 1, 1);
                        quotaItem.setStartDate(dateFormat.format(quotaStartDate.getTime()));

                        if (monthStep % 3 == 1) {
                            quotaItem.setQuotaAmount(300000);
                        } 
                        else if(monthStep % 3 == 2){
                            quotaItem.setQuotaAmount(750000);
                        }
                        else {
                            quotaItem.setQuotaAmount(500000);
                        }

                        lstQuota.add(quotaItem);
                    }

                    currentYear = currentYear + 1;
                }
            }

            // Now we iterate on Pipeline Trending, that is, the opportunity historical data
            while (csvPipeTrendIterator.hasNext()) {
                PipelineTrendingCsv currentOppHist = csvPipeTrendIterator.next();
                String opptyId = currentOppHist.getOpportunityId();

                // Oppty exists?
                if (opptyMap.containsKey(opptyId)) {
                    OpportunityCsv opp = opptyMap.get(opptyId);
                    currentOppHist.setOpportunityData(opp);
                    opp.setRecordTypeName(currentOppHist.getOpportunityRecordTypeName());
                }
                
                lstPipelineTrending.add(currentOppHist);
            }

            // Write Oppty, Quota and Pipeline Trending CSVs
            List<OpportunityCsv> lstOppty = new LinkedList<OpportunityCsv>();
            lstOppty.addAll(opptyMap.values());
            genOpptyBeanToCsv.write(lstOppty);
            genQuotaBeanToCsv.write(lstQuota);
            genPipeTrendBeanToCsv.write(lstPipelineTrending);
        }
    }    
}