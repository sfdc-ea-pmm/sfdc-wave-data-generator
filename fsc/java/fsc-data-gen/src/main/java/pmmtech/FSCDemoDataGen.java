package pmmtech;

import com.opencsv.CSVWriter;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;
import com.opencsv.bean.StatefulBeanToCsv;
import com.opencsv.bean.StatefulBeanToCsvBuilder;
import java.io.Reader;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public class FSCDemoDataGen {
    private static final String SOURCE_ACCOUNTS_CSV_FILE_PATH = "./SourceAccounts.csv";
    private static final String SOURCE_ZIP_AND_STATES_CSV_FILE_PATH = "./SourceZipCodesAndStates.csv";
    private static final String SOURCE_OPPTY_CSV_FILE_PATH = "./SourceOpportunities.csv";
    private static final String SOURCE_PIPELINE_TRENDING_CSV_FILE_PATH = "./SourcePipelineTrending.csv";
    private static final String SOURCE_LEADS_CSV_FILE_PATH = "./SourceLeads.csv";
    private static final String SOURCE_OWNERS_CSV_FILE_PATH = "./SourceOwners.csv";
    private static final String SOURCE_CAMPAIGN_MEMBER_CSV_FILE_PATH = "./SourceCampaignMembers.csv";
    private static final String SOURCE_CAMPAIGN_CSV_FILE_PATH = "./SourceCampaigns.csv";
    private static final String SOURCE_SAMPLE_RECORD_IDS_CSV_FILE_PATH = "./SampleRecordIds.csv";
    private static final String GEN_ACCOUNTS_CSV_FILE_PATH = "./FscDemoAccount.csv";
    private static final String GEN_FIN_ACCOUNTS_CSV_FILE_PATH = "./FscDemoFinancialAccount.csv";
    private static final String GEN_FIN_ACCOUNT_TRNX_CSV_FILE_PATH = "./FscDemoFinancialAccountTransaction.csv";
    private static final String GEN_FIN_GOALS_CSV_FILE_PATH = "./FscDemoFinancialGoal.csv";
    private static final String GEN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH = "./FscDemoAccountSnapshot.csv";
    private static final String GEN_FIN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH = "./FscDemoFinancialAccountSnapshot.csv";
    private static final String GEN_FIN_ACCOUNT_TRN_SNAPSHOT_CSV_FILE_PATH = "./FscDemoFinancialAccountTransactionSnapshot.csv";
    private static final String GEN_FIN_GOALS_SNAPSHOT_CSV_FILE_PATH = "./FscDemoFinancialGoalSnapshot.csv";
    private static final String GEN_ACTIVITIES_CSV_FILE_PATH = "./FscDemoActivity.csv";
    private static final String GEN_LEADS_CSV_FILE_PATH = "./FscDemoLead.csv";
    private static final String GEN_LEAD_HISTORY_CSV_FILE_PATH = "./FscDemoLeadHistory.csv";
    private static final String GEN_EVENTS_CSV_FILE_PATH = "./FscDemoEvent.csv";
    private static final String GEN_CASES_CSV_FILE_PATH = "./FscDemoCase.csv";
    private static final String GEN_CAMPAIGNS_CSV_FILE_PATH = "./FscDemoCampaign.csv";
    private static final String GEN_CAMPAIGN_MEMBERS_CSV_FILE_PATH = "./FscDemoCampaignMember.csv";
    private static final String GEN_OPPTY_CSV_FILE_PATH = "./FscDemoOpportunity.csv";
    private static final String GEN_PIPELINE_TRENDING_CSV_FILE_PATH = "./FscDemoPipelineTrending.csv";    
    private static final String GEN_QUOTA_CSV_FILE_PATH = "./FscDemoQuota.csv";
    private static final int TOTAL_ACCOUNTS_TO_CREATE = 310;
    private static final int MIN_ACCOUNTS_TO_CREATE = 0;
    private static final int MAX_ACCOUNTS_TO_CREATE = 5;
    private static final int MAX_FIN_ACCOUNTS_TO_CREATE = 4;
    private static final int MAX_DAYS_BEHIND_REL_START_DATE = 3650; // 10 years in the past
    private static final int MIN_TRANSACTION_AMOUNT_BANKING_ACCOUNT = 200;
    private static final int MAX_TRANSACTION_AMOUNT_BANKING_ACCOUNT = 500;
    private static final int MIN_TRANSACTION_AMOUNT_INVESTMENT_ACCOUNT = 47000;
    private static final int MAX_TRANSACTION_AMOUNT_INVESTMENT_ACCOUNT = 68000;
    private static final int MAX_DECREASE = MAX_TRANSACTION_AMOUNT_BANKING_ACCOUNT;
    private static final int MAX_DECREASE_FOR_SAMPLE = MAX_TRANSACTION_AMOUNT_BANKING_ACCOUNT;
    private static final int MIN_CONTACT_ANNUAL_INCOME = 50000;
    private static final int MAX_CONTACT_ANNUAL_INCOME = 250000;
    //private static final int MAX_LEADS_PER_WEEK = 10;
    private static final int MIN_NUMBER_SENT_PER_CAMPAIGN = 50;
    private static final int MAX_NUMBER_SENT_PER_CAMPAIGN = 80;
    private static final int FISCAL_YEAR_START_MONTH = 1; // February for Salesforce
    private static final int MAX_RECORDS_AUM_PERCENT = 50;
    private static final int AUM_PERCENT_LESS_THAN = 50; // AUM < 50% of historical AUM
    private static final int MIN_CAMPAIGN_ACTUAL_COST = 5000;
    private static final int MAX_CAMPAIGN_ACTUAL_COST = 20000;

    // Will inspect accounts with Last Review Date in previous fiscal year
    // Will pick max 50
    // On last month of data generation, will put credit transaction so that new AUM < 50% of their max AUM
    
    public static void main(String[] args) throws Exception
    {
        try (
            Reader srcAcctReader = Files.newBufferedReader(Paths.get(SOURCE_ACCOUNTS_CSV_FILE_PATH));
            Reader srcZipStatesReader = Files.newBufferedReader(Paths.get(SOURCE_ZIP_AND_STATES_CSV_FILE_PATH));
            Reader srcOpptyReader = Files.newBufferedReader(Paths.get(SOURCE_OPPTY_CSV_FILE_PATH));
            Reader srcPipeTrendReader = Files.newBufferedReader(Paths.get(SOURCE_PIPELINE_TRENDING_CSV_FILE_PATH));
            Reader srcLeadsReader = Files.newBufferedReader(Paths.get(SOURCE_LEADS_CSV_FILE_PATH));
            Reader srcOwnersReader = Files.newBufferedReader(Paths.get(SOURCE_OWNERS_CSV_FILE_PATH));
            Reader srcSampleRecordIdsReader = Files.newBufferedReader(Paths.get(SOURCE_SAMPLE_RECORD_IDS_CSV_FILE_PATH));
            Reader srcCampaignReader = Files.newBufferedReader(Paths.get(SOURCE_CAMPAIGN_CSV_FILE_PATH));
            Reader srcCampaignMemberReader = Files.newBufferedReader(Paths.get(SOURCE_CAMPAIGN_MEMBER_CSV_FILE_PATH));

            Writer genAcctWriter = Files.newBufferedWriter(Paths.get(GEN_ACCOUNTS_CSV_FILE_PATH));
            Writer genLeadsWriter = Files.newBufferedWriter(Paths.get(GEN_LEADS_CSV_FILE_PATH));
            Writer genFinAcctWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNTS_CSV_FILE_PATH));
            Writer genFinAcctTrnWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNT_TRNX_CSV_FILE_PATH));
            Writer genActivityWriter = Files.newBufferedWriter(Paths.get(GEN_ACTIVITIES_CSV_FILE_PATH));
            Writer genCaseWriter = Files.newBufferedWriter(Paths.get(GEN_CASES_CSV_FILE_PATH));
            Writer genLeadWriter = Files.newBufferedWriter(Paths.get(GEN_LEADS_CSV_FILE_PATH));
            Writer genLeadHistWriter = Files.newBufferedWriter(Paths.get(GEN_LEAD_HISTORY_CSV_FILE_PATH));
            Writer genEventWriter = Files.newBufferedWriter(Paths.get(GEN_EVENTS_CSV_FILE_PATH));
            Writer genCampWriter = Files.newBufferedWriter(Paths.get(GEN_CAMPAIGNS_CSV_FILE_PATH));
            Writer genFinGoalWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_GOALS_CSV_FILE_PATH));
            Writer genOpptyWriter = Files.newBufferedWriter(Paths.get(GEN_OPPTY_CSV_FILE_PATH));
            Writer genPipeTrendWriter = Files.newBufferedWriter(Paths.get(GEN_PIPELINE_TRENDING_CSV_FILE_PATH));
            Writer genQuotaWriter = Files.newBufferedWriter(Paths.get(GEN_QUOTA_CSV_FILE_PATH));
            Writer genAcctSnapWriter = Files.newBufferedWriter(Paths.get(GEN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH)); 
            Writer genFinAcctSnapWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNTS_SNAPSHOT_CSV_FILE_PATH)); 
            Writer genFinAcctTrnSnapWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_ACCOUNT_TRN_SNAPSHOT_CSV_FILE_PATH));
            Writer genFinGoalSnapWriter = Files.newBufferedWriter(Paths.get(GEN_FIN_GOALS_SNAPSHOT_CSV_FILE_PATH));
            Writer genCampMemberWriter = Files.newBufferedWriter(Paths.get(GEN_CAMPAIGN_MEMBERS_CSV_FILE_PATH));
            
            CSVWriter genAcctSnapCsvWriter = new CSVWriter(genAcctSnapWriter,
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.DEFAULT_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END);
                
            CSVWriter genFinAcctSnapCsvWriter = new CSVWriter(genFinAcctSnapWriter,
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.DEFAULT_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END);

            CSVWriter genFinAcctTrnSnapCsvWriter = new CSVWriter(genFinAcctTrnSnapWriter,
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.DEFAULT_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END);

            CSVWriter genFinGoalSnapCsvWriter = new CSVWriter(genFinGoalSnapWriter,
                CSVWriter.DEFAULT_SEPARATOR,
                CSVWriter.DEFAULT_QUOTE_CHARACTER,
                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                CSVWriter.DEFAULT_LINE_END);
        ){
            CsvToBean<SampleRecordIds> sampleRecordIdsCsvToBean = new CsvToBeanBuilder<SampleRecordIds>(srcSampleRecordIdsReader)
                .withType(SampleRecordIds.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<AccountCsv> acctCsvToBean = new CsvToBeanBuilder<AccountCsv>(srcAcctReader)
                .withType(AccountCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<LeadCsv> leadsCsvToBean = new CsvToBeanBuilder<LeadCsv>(srcLeadsReader)
                .withType(LeadCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<UserOwnerCsv> ownersCsvToBean = new CsvToBeanBuilder<UserOwnerCsv>(srcOwnersReader)
                .withType(UserOwnerCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            StatefulBeanToCsv<LeadHistoryCsv> genLeadHistBeanToCsv = new StatefulBeanToCsvBuilder<LeadHistoryCsv>(genLeadHistWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<EventCsv> genEventsBeanToCsv = new StatefulBeanToCsvBuilder<EventCsv>(genEventWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            CsvToBean<ZipAndStateCsv> zipAndStatesCsvToBean = new CsvToBeanBuilder<ZipAndStateCsv>(srcZipStatesReader)
                .withType(ZipAndStateCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<OpportunityCsv> opptyCsvToBean = new CsvToBeanBuilder<OpportunityCsv>(srcOpptyReader)
                .withType(OpportunityCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<CampaignCsv> campCsvToBean = new CsvToBeanBuilder<CampaignCsv>(srcCampaignReader)
                .withType(CampaignCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<CampaignMemberCsv> campMemberCsvToBean = new CsvToBeanBuilder<CampaignMemberCsv>(srcCampaignMemberReader)
                .withType(CampaignMemberCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            CsvToBean<PipelineTrendingCsv> pipeTrendCsvToBean = new CsvToBeanBuilder<PipelineTrendingCsv>(srcPipeTrendReader)
                .withType(PipelineTrendingCsv.class)
                .withIgnoreLeadingWhiteSpace(true)
                .build();

            StatefulBeanToCsv<AccountCsv> genAcctBeanToCsv = new StatefulBeanToCsvBuilder<AccountCsv>(genAcctWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<FinancialAccountCsv> genFinAcctBeanToCsv = new StatefulBeanToCsvBuilder<FinancialAccountCsv>(genFinAcctWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<FinancialGoalCsv> genFinGoalsBeanToCsv = new StatefulBeanToCsvBuilder<FinancialGoalCsv>(genFinGoalWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<FinancialAccountTransactionCsv> genFinAcctTrnBeanToCsv = new StatefulBeanToCsvBuilder<FinancialAccountTransactionCsv>(genFinAcctTrnWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();
                
            StatefulBeanToCsv<ActivityCsv> genActivityBeanToCsv = new StatefulBeanToCsvBuilder<ActivityCsv>(genActivityWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<CaseCsv> genCaseBeanToCsv = new StatefulBeanToCsvBuilder<CaseCsv>(genCaseWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<LeadCsv> genLeadBeanToCsv = new StatefulBeanToCsvBuilder<LeadCsv>(genLeadWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<CampaignCsv> genCampBeanToCsv = new StatefulBeanToCsvBuilder<CampaignCsv>(genCampWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<CampaignMemberCsv> genCampMemberBeanToCsv = new StatefulBeanToCsvBuilder<CampaignMemberCsv>(genCampMemberWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<OpportunityCsv> genOpptyBeanToCsv = new StatefulBeanToCsvBuilder<OpportunityCsv>(genOpptyWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<PipelineTrendingCsv> genPipeTrendBeanToCsv = new StatefulBeanToCsvBuilder<PipelineTrendingCsv>(genPipeTrendWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();

            StatefulBeanToCsv<QuotaCsv> genQuotaBeanToCsv = new StatefulBeanToCsvBuilder<QuotaCsv>(genQuotaWriter)
                .withQuotechar(CSVWriter.DEFAULT_QUOTE_CHARACTER)
                .build();
            
            String[] snapshotDatesHeader = new String[] {
                "SnapshotDate",
                "SnapshotTextDate"
            };
            
            // Snapshot dataset headers
            genAcctSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDatesHeader, AccountCsv.getCsvHeader()));
            genFinAcctSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDatesHeader, FinancialAccountCsv.getCsvHeader()));
            genFinAcctTrnSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDatesHeader, FinancialAccountTransactionCsv.getCsvHeader()));
            genFinGoalSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDatesHeader, FinancialGoalCsv.getCsvHeader()));
            
            Iterator<SampleRecordIds> csvSampleRecordIdsIterator = sampleRecordIdsCsvToBean.iterator();
            Iterator<AccountCsv> csvAccountIterator = acctCsvToBean.iterator();
            Iterator<ZipAndStateCsv> csvZipAndStatesIterator = zipAndStatesCsvToBean.iterator();
            Iterator<UserOwnerCsv> csvOwnersIterator = ownersCsvToBean.iterator();
            Map<String, UserOwnerCsv> advisorsMap = new HashMap<String, UserOwnerCsv>();
            Map<String, List<String>> zipAndStatesTable = new HashMap<String, List<String>>();
            List<ZipAndStateCsv> lstCitiesAndState = new LinkedList<ZipAndStateCsv>();
            List<AccountCsv> lstAccounts = new LinkedList<AccountCsv>();
            List<FinancialAccountCsv> lstFinAccounts = new LinkedList<FinancialAccountCsv>();
            List<String> lstSampleFinAccountIds = new LinkedList<String>();
            List<FinancialAccountCsv> lstSampleFinAccounts = new LinkedList<FinancialAccountCsv>();
            List<FinancialAccountTransactionCsv> lstFinAccountTransactions = new LinkedList<FinancialAccountTransactionCsv>();
            List<ActivityCsv> lstActivities = new LinkedList<ActivityCsv>();
            List<CaseCsv> lstCases = new LinkedList<CaseCsv>();
            List<LeadCsv> lstLeads = new LinkedList<LeadCsv>();
            List<LeadHistoryCsv> lstLeadHistory = new LinkedList<LeadHistoryCsv>();
            List<EventCsv> lstEvents = new LinkedList<EventCsv>();
            List<CampaignCsv> lstCampaigns = new LinkedList<CampaignCsv>();
            List<CampaignMemberCsv> lstCampaignMembers = new LinkedList<CampaignMemberCsv>();
            List<FinancialGoalCsv> lstFinancialGoals = new LinkedList<FinancialGoalCsv>();
            List<FinancialGoalCsv> lstSampleFinancialGoals = new LinkedList<FinancialGoalCsv>();
            Random randHelper = new Random();
            int accountsCreatedCount = 0;
            int accountsToCreateCount = 0;
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
            Calendar startOfPrevFiscalYear = Calendar.getInstance();
            Calendar todayDate = Calendar.getInstance();
            Calendar currentSnapshotDate = Calendar.getInstance();
            currentSnapshotDate.add(Calendar.MONTH, -18); // 1 and 1/2 years to the past
            int weeksCounter = 0;
            int monthsCounter = 0;
            SampleRecordIds sampleRecordsConfig = null;
            startOfPrevFiscalYear.set(Calendar.DAY_OF_MONTH, 1);
            startOfPrevFiscalYear.set(Calendar.MONTH, FISCAL_YEAR_START_MONTH);
            startOfPrevFiscalYear.set(Calendar.YEAR, todayDate.get(Calendar.YEAR) - 1);
            Calendar endOfPrevFiscalYear = (Calendar)startOfPrevFiscalYear.clone();
            endOfPrevFiscalYear.add(Calendar.YEAR, 1);
            endOfPrevFiscalYear.add(Calendar.DAY_OF_MONTH, -1);
            System.out.println("Date of the Prev FY start: " + dateFormat.format(startOfPrevFiscalYear.getTime()));
            System.out.println("Date of the Prev FY end: " + dateFormat.format(endOfPrevFiscalYear.getTime()));
            
            Map<String, AccountCsv> prevFiscalYearReviewedAccounts = new HashMap<String, AccountCsv>();
            Map<String, Double> historicMaxAumByAccount = new HashMap<String, Double>();
            
            if (csvSampleRecordIdsIterator.hasNext()) {
                sampleRecordsConfig = csvSampleRecordIdsIterator.next();
            }
            else {
                throw new Exception("Unable to generate FSC data: No Sample Records Ids file found.");
            }

            while (csvOwnersIterator.hasNext()) {
                UserOwnerCsv currOwner = csvOwnersIterator.next();
                advisorsMap.put(currOwner.getName(), currOwner);
            }

            List<RandomString> advisorNames = new LinkedList<RandomString>();
            RandomString rndString = new RandomString();
            rndString.setRandomString("Chelsea Advisor");
            rndString.setRelativeProbability(20);
            advisorNames.add(rndString);

            rndString = new RandomString();
            rndString.setRandomString("Mark Garet");
            rndString.setRelativeProbability(10);
            advisorNames.add(rndString);

            rndString = new RandomString();
            rndString.setRandomString("Brenda Banker");
            rndString.setRelativeProbability(25);
            advisorNames.add(rndString);

            rndString = new RandomString();
            rndString.setRandomString("Allen Advisor");
            rndString.setRelativeProbability(60);
            advisorNames.add(rndString);

            StringSelectorWithProbability stringSel = new StringSelectorWithProbability(advisorNames);

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
            finAccRt.setRelativeProbability(65);
            finAccRt.setRecordTypeName("Investment Account");
            lstFinAccRecordTypes.add(finAccRt);

            // Credit Card Record Type: Won't be used for now
            //finAccRt = new FinancialAccountRecordType();
            //finAccRt.setRelativeProbability(3);
            //finAccRt.setRecordTypeName("Credit Card");
            //lstFinAccRecordTypes.add(finAccRt);

            // Savings Account Record Type
            finAccRt = new FinancialAccountRecordType();
            finAccRt.setRelativeProbability(15);
            finAccRt.setRecordTypeName("Savings Account");
            lstFinAccRecordTypes.add(finAccRt);

            finAccRt = new FinancialAccountRecordType();
            finAccRt.setRelativeProbability(25);
            finAccRt.setRecordTypeName("Mutual Fund Investment");
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
            Collections.addAll(lstMarketingSegments, "Mass Market", "Affluent Professionals", "High Net Worth Families", "Retired", "Millennials");

            // Customer Segments
            ArrayList<String> lstCustomerSegments = new ArrayList<String>();
            Collections.addAll(lstCustomerSegments, "Long Term Growth", "Mass Affluent");

            // Investment Objectives
            ArrayList<String> lstInvestmentObjectives = new ArrayList<String>();
            Collections.addAll(lstInvestmentObjectives, "Income", "Balanced Growth", "Growth", "Aggressive Growth");

            // Investment Experience
            ArrayList<String> lstInvestmentExperience = new ArrayList<String>();
            Collections.addAll(lstInvestmentExperience, "Experienced", "Moderately Experienced", "Moderately Inexperienced", "Inexperienced");

            // Client Category
            ArrayList<String> lstClientCats = new ArrayList<String>();
            Collections.addAll(lstClientCats, "Platinum", "Gold", "Silver");

            // Review Frequencies
            ArrayList<String> lstReviewFrequencies = new ArrayList<String>();
            Collections.addAll(lstReviewFrequencies, 
                "Monthly", 
                "Quarterly",
                "Annually"
            );

            // Risk Tolerances
            ArrayList<String> lstRiskTolerances = new ArrayList<String>();
            Collections.addAll(lstRiskTolerances, 
                "Aggresive", 
                "Conservative",
                "Moderate",
                "None"
            );

            // Financial Interests
            ArrayList<String> lstFinancialInterests = new ArrayList<String>();
            Collections.addAll(lstFinancialInterests, 
                "Municipal Bonds", 
                "Fixed Income",
                "Energy",
                "Technology",
                "Retirement",
                "College Planning"
            );

            // Activity Regarding
            ArrayList<String> lstActivityRegardings = new ArrayList<String>();
            Collections.addAll(lstActivityRegardings, 
                "Client Retention", 
                "Onboarding",
                "Prospecting",
                "Service"
            );

            // Activity Subject
            ArrayList<String> lstActivitySubjects = new ArrayList<String>();
            Collections.addAll(lstActivitySubjects, 
                "Discussion", 
                "Evaluate Refinancing Loan",
                "Lunch Meeting",
                "Quarterly Earnings Summary",
                "Send Birthday Gift",
                "Summit",
                "Sync Up"
            );

            // Activity Status
            ArrayList<String> lstActivityStatus = new ArrayList<String>();
            Collections.addAll(lstActivityStatus, 
                "Not Started", 
                "Open",
                "In Progress",
                "Completed"
            );

            // Campaign type
            ArrayList<String> lstCampaignType = new ArrayList<String>();
            Collections.addAll(lstCampaignType, 
                "Event", 
                "Seminar / Conference"
            );

            // Campaign Member type
            ArrayList<String> lstCampaignMemberType = new ArrayList<String>();
            Collections.addAll(lstCampaignMemberType, 
                "Prospect", 
                "Contact",
                "Lead and Referral"
            );

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

            // Financial Account Ownerships
            ArrayList<String> lstFinAcctsOwnerships = new ArrayList<String>();
            Collections.addAll(lstFinAcctsOwnerships, 
                "Individual", 
                //"Joint", // not used for now
                "Trust"
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
            
            // FIRST PART
            
            // We are gonna generate data for each week from one year in the past until today
            List<Calendar> lstDatesToProcess = new LinkedList<Calendar>();

            while (currentSnapshotDate.compareTo(todayDate) <= 0) {
                lstDatesToProcess.add((Calendar)currentSnapshotDate.clone());
                currentSnapshotDate.add(Calendar.WEEK_OF_YEAR, 1); // Step one week to the future
            }

            if (currentSnapshotDate.compareTo(todayDate) > 0) {
                // We add the latest snapshot for TODAY
                lstDatesToProcess.add((Calendar)todayDate.clone());
            }

            Iterator<CampaignCsv> csvCampaignIterator = campCsvToBean.iterator();
            Iterator<CampaignMemberCsv> csvCampMembeIterator = campMemberCsvToBean.iterator();
            
            for (int cantIterations = 0; cantIterations < lstDatesToProcess.size(); cantIterations++) {
                
                currentSnapshotDate = lstDatesToProcess.get(cantIterations);
                weeksCounter++;
                
                if(lstAccounts.size() > 0){
                    
                    // First of all, tweak the existing business. We are gonna remove some existing accounts
                    if (weeksCounter == 4) {
                        int cantItemsToRemove = Helper.getRandomNumberInRange(0, 10);
                        List<Integer> lstAcctIndexesToRemove = Helper.getRandomIndexesList(lstAccounts.size(), cantItemsToRemove);
                        List<AccountCsv> lstAccountsToRemove = new LinkedList<AccountCsv>();
                        
                        for (Integer index : lstAcctIndexesToRemove) {
                            AccountCsv accToRemove = lstAccounts.get(index);
                            if (!accToRemove.isSampleAccount() && !prevFiscalYearReviewedAccounts.containsKey(accToRemove.getId())) {
                                lstAccountsToRemove.add(accToRemove);
                            } // We won't delete sample special accounts that are part of the story                            
                        }
                        
                        lstAccounts.removeAll(lstAccountsToRemove);
                        
                        List<String> lstAccountIdsToRemove = new LinkedList<String>();
                        for (AccountCsv var : lstAccountsToRemove) {
                            lstAccountIdsToRemove.add(var.getId());
                        }

                        List<FinancialAccountCsv> lstFinAcctsToRemove = new LinkedList<FinancialAccountCsv>();
                        for (FinancialAccountCsv var : lstFinAccounts) {
                            if (lstAccountIdsToRemove.contains(var.getAccountId())) {
                                lstFinAcctsToRemove.add(var);
                            }
                        }

                        lstFinAccounts.removeAll(lstFinAcctsToRemove);

                        List<FinancialAccountTransactionCsv> lstTransToRemove = new LinkedList<FinancialAccountTransactionCsv>();
                        for (FinancialAccountTransactionCsv var : lstFinAccountTransactions) {
                            if (lstAccountIdsToRemove.contains(var.getAccountId())) {
                                lstTransToRemove.add(var);
                            }
                        }

                        lstTransToRemove.removeAll(lstTransToRemove);

                        // And make Financial Goals move forward
                        for (FinancialGoalCsv  sampleFinGoal: lstSampleFinancialGoals) {
                            int actualValue = sampleFinGoal.getActualValue();
                            int targetValue = sampleFinGoal.getFinalActualValue();
                            int amountToReach = targetValue - actualValue;
                            if (amountToReach > 0) {
                                int amountToAdd = Helper.getRandomNumberInRange(0, amountToReach);
                                if (amountToAdd > 0) {
                                    sampleFinGoal.setActualValue(actualValue + amountToAdd);
                                }
                            }
                        }
                    }

                    // Then change the remaining ones
                    int cantItemsToChange = Helper.getRandomNumberInRange(0, lstAccounts.size());
                    List<Integer> lstAcctIndexesToChange = Helper.getRandomIndexesList(lstAccounts.size(), cantItemsToChange);
                    
                    // We will also add those accounts which have heldaway/total fin accounts < 0.3
                    for (int i = 0; i < lstAccounts.size(); i++) {
                        AccountCsv acctToInspect = lstAccounts.get(i);
                        
                        double heldAwayPrc = acctToInspect.getHeldAway() / acctToInspect.getTotalFinancialAccounts();
                        if (heldAwayPrc < 0.3 && !lstAcctIndexesToChange.contains(i)) {
                            lstAcctIndexesToChange.add(i);
                        }

                        if (cantIterations == lstDatesToProcess.size() - 1) {
                            // Last snapshot, we need to make sample financial accounts match their balances
                            Set<String> sampleFinancialAccountsAccountIds = new HashSet<String>();
                            for (FinancialAccountCsv sampleFinAcc : lstSampleFinAccounts) {
                                sampleFinancialAccountsAccountIds.add(sampleFinAcc.getAccountId());
                            }

                            // This account has one of the sample financial accounts, so it must be altered
                            if (sampleFinancialAccountsAccountIds.contains(acctToInspect.getId())) {
                                lstAcctIndexesToChange.add(i);
                            }

                            // Accounts with Last Review Date in previous fiscal year
                            Date dLastReview = dateFormat.parse(acctToInspect.getLastReview());
                            Calendar calLastReview = Calendar.getInstance();
                            calLastReview.setTime(dLastReview);

                            if (!acctToInspect.isSampleAccount() && calLastReview.compareTo(startOfPrevFiscalYear) >= 0 && calLastReview.compareTo(endOfPrevFiscalYear) <= 0 && prevFiscalYearReviewedAccounts.keySet().size() < MAX_RECORDS_AUM_PERCENT) {
                                // This account has last review in previous fiscal year
                                prevFiscalYearReviewedAccounts.put(acctToInspect.getId(), acctToInspect);

                                if (!lstAcctIndexesToChange.contains(i)) {
                                    lstAcctIndexesToChange.add(i);
                                }
                            }
                        }

                        // Sample accounts: always
                        if (acctToInspect.isSampleAccount() && !lstAcctIndexesToChange.contains(i)) {
                            lstAcctIndexesToChange.add(i);
                        }
                    }
                    
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
                            
                            if ((cantIterations == lstDatesToProcess.size() - 1 && lstSampleFinAccountIds.contains(finAcctToChange.getId())) || ((!finAcctToChange.isHeldAway() && weeksCounter == 2) || (finAcctToChange.isHeldAway() && weeksCounter == 4)) || (!prevFiscalYearReviewedAccounts.containsKey(acctToChange.getId()))) {
                                // We will add transaction if:
                                // Last snapshot and financial account has to be adjusted to its demo balance
                                // Is not held away
                                // Is held away and we elapsed a month
                                // Account is not part of the set that has last review in previous fiscal year and we have to make its AUM go less than 50% of its historic max
                                // Random Updates to held away accounts occur once a month
                                // We add a new transaction to the account
                                FinancialAccountTransactionCsv t = new FinancialAccountTransactionCsv();
                                t.setId("Trnx-" + finAcctToChange.getTransactions().size() + "-" + finAcctToChange.getId());
                                t.setAccountData(acctToChange);
                                t.setFinancialAccountId(finAcctToChange.getId());
                                t.setFinancialAccountType(finAcctToChange.getFinancialAccountType());
                                t.setOwnerName(acctToChange.getOwnerName());
                                
                                Double dblBalance = Double.valueOf(balance);
                                int rndDirection = Helper.getRandomNumberInRange(-1, 1);
                                double trnxAmount = 0;

                                if (cantIterations == lstDatesToProcess.size() - 1 && lstSampleFinAccountIds.contains(finAcctToChange.getId())) {
                                    
                                    double balanceDifference = 0;
                                    
                                    if (finAcctToChange.getId().equals(sampleRecordsConfig.getMutualFundInvestment())) {
                                        // Mutual Fund Investment
                                        // Balance 142000
                                        balanceDifference = 142000 - balance;
                                    } 
                                    else if(finAcctToChange.getId().equals(sampleRecordsConfig.getSavingsAccount())){
                                        // Savings Account
                                        // Balance 5570
                                        balanceDifference = 5570 - balance; 
                                    }
                                    else if(finAcctToChange.getId().equals(sampleRecordsConfig.getBankOfBasCheckingAccount())){
                                        // Bank of BAS Checking Account
                                        // Balance 100000
                                        balanceDifference = 100000 - balance;
                                    }
                                    else if(finAcctToChange.getId().equals(sampleRecordsConfig.getInvestmentAccount())){
                                        // Investment Account
                                        // Balance 895000
                                        balanceDifference = 895000 - balance;
                                    }
                                    else if(finAcctToChange.getId().equals(sampleRecordsConfig.getNigelsInvestmentAccount())){
                                        // Nigel's Investment Account
                                        // Balance 300000
                                        balanceDifference = 300000 - balance;
                                    }
                                    else if(finAcctToChange.getId().equals(sampleRecordsConfig.getCreditCard())){
                                        // CreditCard
                                        // Balance 3200
                                        balanceDifference = 3200 - balance;
                                    }

                                    trnxAmount = Math.abs(balanceDifference);
                                    if (balanceDifference < 0) {
                                        t.setTransactionType("Debit");
                                    } 
                                    else {
                                        t.setTransactionType("Credit"); 
                                    }
                                } 
                                else {
                                    // Handle the account's held away trending
                                    if (!acctToChange.getHeldAwayWillIncrease() && finAcctToChange.isHeldAway() && weeksCounter == 4) {
                                        // The held away is set to decrease
                                        rndDirection = -1;
                                    }

                                    double heldAwayPrc = acctToChange.getHeldAway() / totalFinAcctsPrimaryOwner;
                                    double heldAwayFactorToIncrease = 1;

                                    if (finAcctToChange.isHeldAway() && weeksCounter == 4 && heldAwayPrc < 0.3) {
                                        // Will increase
                                        rndDirection = 1;
                                        heldAwayFactorToIncrease = 0.3 * totalFinAcctsPrimaryOwner;
                                    }

                                    if (rndDirection < 0 && dblBalance.intValue() > 1) {
                                        t.setTransactionType("Debit");                                    
                                        int iBalance = dblBalance.intValue();
                                        int amountToSubstract = MAX_DECREASE;
                                        
                                        if (acctToChange.isSampleAccount()) {
                                            amountToSubstract = MAX_DECREASE_FOR_SAMPLE;
                                        }

                                        if (amountToSubstract > iBalance) {
                                            amountToSubstract = iBalance;
                                        }
                                        
                                        trnxAmount = Helper.getRandomNumberInRange(1, amountToSubstract);
                                    } 
                                    else {
                                        t.setTransactionType("Credit");
                                        if (heldAwayFactorToIncrease != 1 && finAcctToChange.isHeldAway()) {
                                            trnxAmount = heldAwayFactorToIncrease;
                                        }
                                        else {
                                            
                                            if (acctToChange.isSampleAccount()) {
                                                if (finAcctToChange.getFinancialAccountType().equals("Bank Account") || finAcctToChange.getFinancialAccountType().equals("Savings Account")) {
                                                    // trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT_FOR_SAMPLE, MAX_TRANSACTION_AMOUNT_FOR_SAMPLE); // ORIGINAL LINE
                                                    trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT_BANKING_ACCOUNT, MAX_TRANSACTION_AMOUNT_BANKING_ACCOUNT);
                                                }
                                                else { // For Mutual Funds & Investments
                                                    trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT_INVESTMENT_ACCOUNT, MAX_TRANSACTION_AMOUNT_INVESTMENT_ACCOUNT);
                                                }
                                                
                                            } 
                                            else { 
                                                trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT_BANKING_ACCOUNT, MAX_TRANSACTION_AMOUNT_BANKING_ACCOUNT);
                                            }
                                        }
                                    }

                                }

                                if (trnxAmount > 0) {
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
                        }

                        acctToChange.setTotalFinAcctsPrimaryOwner(totalFinAcctsPrimaryOwner);
                        acctToChange.setTotalAUMPrimaryOwner(totalAUMPrimaryOwner);
                        acctToChange.setTotalHeldFinAcctsPrimaryOwner(totalHeldFinAcctsPrimaryOwner);

                        if (prevFiscalYearReviewedAccounts.containsKey(acctToChange.getId()) && acctToChange.getFinancialAccounts().size() > 0) {
                            
                            double accCurrentAum = acctToChange.getAum();

                            if (historicMaxAumByAccount.containsKey(acctToChange.getId())) {
                                double accMaxAum = historicMaxAumByAccount.get(acctToChange.getId());
                                double accAumMaxTarget = accMaxAum * AUM_PERCENT_LESS_THAN / 100;

                                System.out.println("Need to reduce AUM for account: " + acctToChange.getName());
                                System.out.println("Take it to less than: " + accAumMaxTarget);
                                
                                if(accAumMaxTarget > 0){
                                    // the AUM range could be enforced here //oz.
                                    while (accCurrentAum >= accAumMaxTarget) {
                                        
                                        System.out.println("Current AUM: " + accCurrentAum);

                                        // Need to start decreasing account AUM to make it reach less than 50% of historic max
                                        int finAcctsCount = acctToChange.getFinancialAccounts().size();
                                        int finAcctIndexToUse = 0;
                                        if (finAcctsCount > 1) {
                                            finAcctIndexToUse = Helper.getRandomNumberInRange(0, finAcctsCount - 1);
                                        }

                                        FinancialAccountCsv finAcctToDecrease = acctToChange.getFinancialAccounts().get(finAcctIndexToUse);

                                        if (finAcctToDecrease.isManaged()) {
                                            double balance = finAcctToDecrease.getBalance();
                                            FinancialAccountTransactionCsv t = new FinancialAccountTransactionCsv();
                                            t.setId("Trnx-" + finAcctToDecrease.getTransactions().size() + "-" + finAcctToDecrease.getId());
                                            t.setAccountData(acctToChange);
                                            t.setFinancialAccountId(finAcctToDecrease.getId());
                                            t.setFinancialAccountType(finAcctToDecrease.getFinancialAccountType());
                                            t.setOwnerName(acctToChange.getOwnerName());
                                            
                                            Double dblBalance = Double.valueOf(balance);
                                            
                                            double trnxAmount = 0;
                                            t.setTransactionType("Debit");                                    
                                            int iBalance = dblBalance.intValue();
                                            int amountToSubstract = MAX_DECREASE;                                        
                                            
                                            if (amountToSubstract > iBalance) {
                                                amountToSubstract = iBalance;
                                            }
                                            
                                            if (amountToSubstract > 1) {
                                                trnxAmount = Helper.getRandomNumberInRange(1, amountToSubstract);
                                            }

                                            if (trnxAmount > 0) {
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
                                                finAcctToDecrease.getTransactions().add(t);
                                                finAcctToDecrease.setBalance(financialAccountBalance);
                                                
                                                totalAUMPrimaryOwner += arithmeticAmount;        
                                                totalFinAcctsPrimaryOwner += arithmeticAmount;

                                                acctToChange.setTotalFinAcctsPrimaryOwner(totalFinAcctsPrimaryOwner);
                                                acctToChange.setTotalAUMPrimaryOwner(totalAUMPrimaryOwner);
                                                accCurrentAum = acctToChange.getAum();

                                                System.out.println("Generated debit for: " + trnxAmount);
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Set max AUM
                        if (historicMaxAumByAccount.containsKey(acctToChange.getId())) {
                            Double accountAum = acctToChange.getAum();
                            Double currentMax = historicMaxAumByAccount.get(acctToChange.getId());
                            if (accountAum > currentMax) {
                                historicMaxAumByAccount.put(acctToChange.getId(), accountAum);
                            }
                        }
                        else {
                            historicMaxAumByAccount.put(acctToChange.getId(), acctToChange.getAum());
                        }

                        if(weeksCounter == 4){
                            
                            // Add some activities to the account, monthly
                            int cntActivitiesToAdd = Helper.getRandomNumberInRange(0, 1);
                            for (int a = 0; a < cntActivitiesToAdd; a++) {
                                                            
                                String rndActivityType = lstActivityTypes.get(Helper.getRandomNumberInRange(0, lstActivityTypes.size() - 1));
                                String rndActivityRegarding = lstActivityRegardings.get(Helper.getRandomNumberInRange(0, lstActivityRegardings.size() - 1));
                                String rndActivitySubject = lstActivitySubjects.get(Helper.getRandomNumberInRange(0, lstActivitySubjects.size() - 1));
                                int activityDaysBefore = Helper.getRandomNumberInRange(1, 29); // Within a month
                                Calendar calActivityDate = (Calendar)currentSnapshotDate.clone();
                                calActivityDate.add(Calendar.DAY_OF_MONTH, -activityDaysBefore);
                                int rndEventOrTask = Helper.getRandomNumberInRange(0, 1);

                                ActivityCsv actToCreate = new ActivityCsv();
                                actToCreate.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                                actToCreate.setAccountData(acctToChange);
                                actToCreate.setAccountType("Customer");
                                actToCreate.setId("Activity-" + acctToChange.getActivities().size() + "-" + acctToChange.getId());                            
                                actToCreate.setActivityDate(dateFormat.format(calActivityDate.getTime()));
                                actToCreate.setType(rndActivityType);
                                actToCreate.setRegarding(rndActivityRegarding);
                                actToCreate.setSubject(rndActivitySubject);

                                // Activity Owner
                                RandomString rndStringSelected = stringSel.getRandomString();
                                UserOwnerCsv rndOwner = advisorsMap.get(rndStringSelected.getRandomString());
                                actToCreate.setOwnerData(rndOwner);

                                if (rndEventOrTask == 0) {
                                    // Event
                                    actToCreate.setRecordTypeName("Advisor Event");
                                    actToCreate.setStatus("Event");
                                    actToCreate.setTaskSubtype("Event");
                                    actToCreate.setPriority("Event");
                                    actToCreate.setEventSubtype("Event");
                                    if (actToCreate.getType().equals("Call")) {
                                        actToCreate.setEventSubtype("Call");
                                        actToCreate.setSubject("Call " + acctToChange.getName());
                                    }
                                }
                                else {
                                    // Task
                                    actToCreate.setRecordTypeName("Advisor Task");
                                    actToCreate.setEventSubtype("Event");
                                    actToCreate.setTaskSubtype("Task");
                                    if (actToCreate.getType().equals("Call")) {
                                        actToCreate.setTaskSubtype("Call");
                                        actToCreate.setSubject("Call " + acctToChange.getName());
                                    }
                                    
                                    int rndPriority = Helper.getRandomNumberInRange(0, 1);
                                    if (rndPriority == 0) {
                                        actToCreate.setPriority("Normal");
                                    }
                                    else {
                                        actToCreate.setPriority("High");
                                    }

                                    String rndTaskStatus = lstActivityStatus.get(Helper.getRandomNumberInRange(0, lstActivityStatus.size() - 1));
                                    actToCreate.setStatus(rndTaskStatus);
                                }

                                lstActivities.add(actToCreate);
                                acctToChange.getActivities().add(actToCreate);
                            }

                            // Review and Interaction dates, also monthly
                            if (acctToChange.getWillHaveReview() && !prevFiscalYearReviewedAccounts.containsKey(acctToChange.getId())) {
                                // Only for those accounts that we don't want to stay unreviewed since last FY
                                acctToChange.generateReviewAndInteractionDates(currentSnapshotDate);
                            }
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
                    
                    // How many accounts are we gonna add?
                    accountsToCreateCount = Helper.getRandomNumberInRange(MIN_ACCOUNTS_TO_CREATE, MAX_ACCOUNTS_TO_CREATE);
                }
                else {
                    accountsToCreateCount = 400;
                }
                // NEW ACCOUNTS (CLIENTS)                
                
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
                    demoAccount.setLeadOrContactId(sourceCsvAccount.getLeadOrContactId());
                    if (sourceCsvAccount.getLeadOrContactId() == null || sourceCsvAccount.getLeadOrContactId().equals("")) {
                        // Default Lead Or Contact Id
                        demoAccount.setLeadOrContactId(sampleRecordsConfig.getDefaultLeadOrContactId());
                    }
                    
                    demoAccount.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                    demoAccount.setInvestmentExperience(sourceCsvAccount.getInvestmentExperience());
                    demoAccount.setInvestmentObjectives(sourceCsvAccount.getInvestmentObjectives());
                    demoAccount.setName(sourceCsvAccount.getName());

                    if (demoAccount.getName().contains(" (Sample)")) {
                        demoAccount.setSampleAccount(true);
                        System.out.println("Found Sample Account: " + demoAccount.getName());
                        demoAccount.setName(sourceCsvAccount.getName().replace(" (Sample)", ""));
                    } 
                    else {
                        demoAccount.setSampleAccount(false);

                        // Random account, let's set if will have review
                        int rndWillHaveReview = Helper.getRandomNumberInRange(1, 100);
                        if (rndWillHaveReview <= 25) {
                            demoAccount.setWillHaveReview(true);
                        }
                    }
                    
                    if (demoAccount.getName().contains("Household")) {
                        demoAccount.setRecordTypeName("Household");
                    } 
                    else {
                        demoAccount.setRecordTypeName(rndAcctRecTypeSel.getRandomAccountRecordType().getRecordTypeName());
                    }

                    if (demoAccount.getRecordTypeName().equals("Household")) {
                        demoAccount.setRollupHouseHoldName(demoAccount.getName());
                        int rndHouseHoldSize = Helper.getRandomNumberInRange(2, 4);
                        demoAccount.setHouseholdSize(rndHouseHoldSize);
                        demoAccount.setHouseholdSizeText(String.valueOf(rndHouseHoldSize));
                        demoAccount.setHouseholdComputed(demoAccount.getName());
                    }
                    else {
                        demoAccount.setHouseholdSize(0);
                        demoAccount.setHouseholdSizeText("0");
                    }        
                    
                    demoAccount.setRelationshipStartDate(dateFormat.format(dtRelStartDate));
                    demoAccount.setYearsSinceClient(Helper.getDiffYears(dtRelStartDate, currentSnapshotDate.getTime()));
                    
                    RandomString rndStringSelected = stringSel.getRandomString();
                    UserOwnerCsv rndOwner = advisorsMap.get(rndStringSelected.getRandomString());
                    demoAccount.setOwnerData(rndOwner);

                    String rndRiskTolerance = lstRiskTolerances.get(Helper.getRandomNumberInRange(0, lstRiskTolerances.size() - 1));
                    demoAccount.setRiskTolerance(rndRiskTolerance);

                    String rndReviewFrequency = lstReviewFrequencies.get(Helper.getRandomNumberInRange(0, lstReviewFrequencies.size() - 1));
                    demoAccount.setReviewFrequency(rndReviewFrequency);
                    
                    String currMarkSeg = lstMarketingSegments.get(Helper.getRandomNumberInRange(0, lstMarketingSegments.size() - 1));
                    demoAccount.setMarketingSegment(currMarkSeg);

                    String currCustSeg = lstCustomerSegments.get(Helper.getRandomNumberInRange(0, lstCustomerSegments.size() - 1));
                    demoAccount.setCustomerSegment(currCustSeg);
                    
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
                    demoAccount.generateReviewAndInteractionDates(currentSnapshotDate);

                    // What are we gonna do with held away? Which will be the trending?
                    int rndHeldAwayTrending = Helper.getRandomNumberInRange(0, 1);
                    demoAccount.setHeldAwayWillIncrease(rndHeldAwayTrending == 1);

                    if (demoAccount.getFinancialInterests() == null || demoAccount.getFinancialInterests().equals("")) {
                        String rndFinInterests = lstFinancialInterests.get(Helper.getRandomNumberInRange(0, lstFinancialInterests.size() - 1));
                        demoAccount.setFinancialInterests(rndFinInterests);
                    }
                    demoAccount.setBillingCountry("USA");

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

                    int finAccToCreateCount = Helper.getRandomNumberInRange(2, MAX_FIN_ACCOUNTS_TO_CREATE);

                    // Before creating financial accounts, we need to make sure that at least one will be held away
                    // to avoid Wallet Share = 0 accounts
                    List<Boolean> heldAwayItems = new LinkedList<Boolean>();
                    int heldAwayCount = 0;
                    for (int b = 0; b < finAccToCreateCount; b++) {
                        Boolean heldAwayRandom = rndHeldAway.getRandomHeldAwayItem().getHeldAway();
                        if (heldAwayRandom) {
                            heldAwayCount++;
                        }
                        heldAwayItems.add(heldAwayRandom);
                    }

                    if (heldAwayCount == 0) {
                        // If no heldaway were selected, we will have at least one
                        heldAwayItems.add(true); 
                    }

                    Boolean addedSampleFinAccount = false;
                    
                    for (int j = 0; j < heldAwayItems.size(); j++) {
                        FinancialAccountCsv finAcct = new FinancialAccountCsv();
                        //finAcct.setId("FinAcct-" + demoAccount.getId() + "-" + j);
                        finAcct.setAccountData(demoAccount);
                        UserOwnerCsv acctOwner = advisorsMap.get(demoAccount.getOwnerName());
                        finAcct.setOwnerData(acctOwner);

                        // Financial Account Created Date
                        int finAccDaysBefore = Helper.getRandomNumberInRange(1, 6);
                        Calendar calFinAccDate = (Calendar)currentSnapshotDate.clone();
                        calFinAccDate.add(Calendar.DAY_OF_MONTH, -finAccDaysBefore);
                        finAcct.setCreatedDate(dateFormat.format(calFinAccDate.getTime()));
                        
                        String rndFinAcctRecType = "";
                        if (!addedSampleFinAccount && demoAccount.getId().equals(sampleRecordsConfig.getNigelAdamsId())) {
                            // Nigel Adams
                            rndFinAcctRecType = "Investment Account";
                        }
                        else {
                            rndFinAcctRecType = rndFinAcctRecTypeSel.getRandomFinancialAccountRecordType().getRecordTypeName();
                        }
                        
                        finAcct.setRecordTypeName(rndFinAcctRecType);

                        // Financial Account Types
                        ArrayList<String> lstFinAccountTypes = new ArrayList<String>();                        
                                               
                        switch (rndFinAcctRecType) {
                            case "Investment Account":
                                // Nigel Adams
                                if (!addedSampleFinAccount && demoAccount.getId().equals(sampleRecordsConfig.getNigelAdamsId())) {
                                    // One of the sample financial accounts: Nigel's Investment Account (Sample)
                                    addedSampleFinAccount = true;
                                    finAcct.setId(sampleRecordsConfig.getNigelsInvestmentAccount());
                                    lstSampleFinAccountIds.add(sampleRecordsConfig.getNigelsInvestmentAccount());
                                    lstSampleFinAccounts.add(finAcct);
                                    finAcct.setFinancialAccountType("Brokerage");
                                }
                                else {
                                    if (!lstSampleFinAccountIds.contains(sampleRecordsConfig.getInvestmentAccount())) {
                                        // One of the sample financial accounts: Investment Account (Sample)
                                        finAcct.setId(sampleRecordsConfig.getInvestmentAccount());
                                        lstSampleFinAccountIds.add(sampleRecordsConfig.getInvestmentAccount());
                                        lstSampleFinAccounts.add(finAcct);
                                    }                                    
                                    
                                    Collections.addAll(lstFinAccountTypes, 
                                        "Brokerage",                                    
                                        "Mutual Fund",
                                        "Fixed Annuity",
                                        "Managed Account"
                                    );
                                }                                
                                break;

                            //case  "Credit Card":
                            //    finAcct.setId("a082E00000XzOlnQAF");
                            //    finAcct.setFinancialAccountType("Credit Card");
                            //    break;

                            case "Bank Account":
                                
                                if (!lstSampleFinAccountIds.contains(sampleRecordsConfig.getBankOfBasCheckingAccount())) {
                                    // One of the sample financial accounts: Bank of BAS Checking Account (Sample)
                                    finAcct.setId(sampleRecordsConfig.getBankOfBasCheckingAccount());
                                    lstSampleFinAccountIds.add(sampleRecordsConfig.getBankOfBasCheckingAccount());
                                    lstSampleFinAccounts.add(finAcct);
                                }

                                Collections.addAll(lstFinAccountTypes, 
                                    "Cash Management Account", 
                                    "Checking"
                                );
                                break;
                            
                            case "Savings Account":
                                
                                if (!lstSampleFinAccountIds.contains(sampleRecordsConfig.getSavingsAccount())) {
                                    // One of the sample financial accounts: Savings Account (Sample)
                                    finAcct.setId(sampleRecordsConfig.getSavingsAccount());
                                    lstSampleFinAccountIds.add(sampleRecordsConfig.getSavingsAccount());
                                    lstSampleFinAccounts.add(finAcct);
                                }

                                finAcct.setFinancialAccountType("Savings");
                                break;

                            case "Mutual Fund Investment":
                                
                                if (!lstSampleFinAccountIds.contains(sampleRecordsConfig.getMutualFundInvestment())){
                                    // One of the sample financial accounts: Mutual Fund Investment (Sample)
                                    finAcct.setId(sampleRecordsConfig.getMutualFundInvestment());
                                    lstSampleFinAccountIds.add(sampleRecordsConfig.getMutualFundInvestment());
                                    lstSampleFinAccounts.add(finAcct);
                                }
                                finAcct.setFinancialAccountType("Mutual Fund");
                                break;
                                
                        }

                        if (finAcct.getId() == null || finAcct.getId().equals("")) {
                            // We make sure to assign an Id for those which aren't sample financial accounts
                            finAcct.setId("FinAcct-" + demoAccount.getId() + "-" + j);
                        }

                        if (finAcct.getFinancialAccountType() == null || finAcct.getFinancialAccountType().equals("")) {
                            String rndFinAcctType = lstFinAccountTypes.get(Helper.getRandomNumberInRange(0, lstFinAccountTypes.size() - 1));
                            finAcct.setFinancialAccountType(rndFinAcctType);
                        }

                        // Held Away based on previously randomly assigned value
                        finAcct.setHeldAway(heldAwayItems.get(j));
                        finAcct.setManaged(!finAcct.isHeldAway());
                        
                        String rndFinAcctOwnership = lstFinAcctsOwnerships.get(Helper.getRandomNumberInRange(0, lstFinAcctsOwnerships.size() - 1));
                        finAcct.setOwnership(rndFinAcctOwnership);

                        double financialAccountBalance = 0;
                        // @TODO: JointOwner

                        // Financial Account Transactions
                        int trxToCreateCount = Helper.getRandomNumberInRange(1, 5);
                        
                        for (int k = 0; k < trxToCreateCount; k++) {
                            FinancialAccountTransactionCsv transaction = new FinancialAccountTransactionCsv();
                            transaction.setId("Trnx-" + k + "-" + finAcct.getId());
                            transaction.setAccountData(demoAccount);
                            transaction.setFinancialAccountId(finAcct.getId());
                            transaction.setFinancialAccountType(finAcct.getFinancialAccountType());
                            transaction.setOwnerName(demoAccount.getOwnerName());
                            
                            // Transaction Type, now are all credits
                            transaction.setTransactionType("Credit");

                            // Transaction Date now() down to 6 days before
                            int trnxDaysBefore = Helper.getRandomNumberInRange(1, 6);
                            Calendar calTrnxDate = (Calendar)currentSnapshotDate.clone();
                            calTrnxDate.add(Calendar.DAY_OF_MONTH, -trnxDaysBefore);
                            transaction.setTransactionDate(dateFormat.format(calTrnxDate.getTime()));
                            
                            // Transaction Amount
                            int trnxAmount;
                            if (transaction.getFinancialAccountType().equals("Bank Account") || transaction.getFinancialAccountType().equals("Savings Account")) {
                                trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT_BANKING_ACCOUNT, MAX_TRANSACTION_AMOUNT_BANKING_ACCOUNT);
                            }
                            else { // For Mutual Funds & Investments
                                trnxAmount = Helper.getRandomNumberInRange(MIN_TRANSACTION_AMOUNT_INVESTMENT_ACCOUNT, MAX_TRANSACTION_AMOUNT_INVESTMENT_ACCOUNT);
                            }
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

                    // Set max AUM
                    historicMaxAumByAccount.put(demoAccount.getId(), demoAccount.getAum());

                    // Financial Goals
                    
                    FinancialGoalCsv finGoal = null;

                    if (demoAccount.getId().equals(sampleRecordsConfig.getNigelAdamsId())) {
                        // Nigel Adams
                        finGoal = new FinancialGoalCsv();
                        finGoal.setAccountData(demoAccount);
                        finGoal.setActualValue(75000);
                        finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                        finGoal.setId(sampleRecordsConfig.getEducationSavingsForMatt());
                        finGoal.setName("Education Savings for Matt");
                        finGoal.setTargetDate("2021-05-26");
                        finGoal.setTargetValue(300000);
                        finGoal.setFinalActualValue(75000);
                        finGoal.setType("Education");
                        lstFinancialGoals.add(finGoal);
                        lstSampleFinancialGoals.add(finGoal);
                    } 
                    else if(demoAccount.getId().equals(sampleRecordsConfig.getJustinSmith())){
                        // Justin Smith
                        finGoal = new FinancialGoalCsv();
                        finGoal.setAccountData(demoAccount);
                        finGoal.setActualValue(37000);
                        finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                        finGoal.setId(sampleRecordsConfig.getHomePurchaseSample());
                        finGoal.setName("Home Purchase");
                        finGoal.setTargetDate("2021-01-01");
                        finGoal.setTargetValue(200000);
                        finGoal.setFinalActualValue(37000);
                        finGoal.setType("Home Purchase");
                        lstFinancialGoals.add(finGoal);
                        lstSampleFinancialGoals.add(finGoal);
                    }
                    else if(demoAccount.getId().equals(sampleRecordsConfig.getNeilSymonds())){
                        // Neil Symonds
                        finGoal = new FinancialGoalCsv();
                        finGoal.setAccountData(demoAccount);
                        finGoal.setActualValue(532000);
                        finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                        finGoal.setId(sampleRecordsConfig.getRetirementGoals());
                        finGoal.setName("Retirement Goals");
                        finGoal.setTargetDate("2019-02-12");
                        finGoal.setTargetValue(540000);
                        finGoal.setFinalActualValue(532000);
                        finGoal.setType("Retirement");
                        lstFinancialGoals.add(finGoal);
                        lstSampleFinancialGoals.add(finGoal);
                    }
                    else if(demoAccount.getId().equals(sampleRecordsConfig.getRachelAdams())){
                        // Rachel Adams has 3
                        finGoal = new FinancialGoalCsv();
                        finGoal.setAccountData(demoAccount);
                        finGoal.setActualValue(67000);
                        finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                        finGoal.setId(sampleRecordsConfig.getLauraWeddingFund());
                        finGoal.setName("Laura's Wedding Fund");
                        finGoal.setTargetDate("2020-05-25");
                        finGoal.setTargetValue(100000);
                        finGoal.setFinalActualValue(67000);
                        finGoal.setType("Other");
                        lstFinancialGoals.add(finGoal);
                        lstSampleFinancialGoals.add(finGoal);

                        finGoal = new FinancialGoalCsv();
                        finGoal.setAccountData(demoAccount);
                        finGoal.setActualValue(150000);
                        finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                        finGoal.setId(sampleRecordsConfig.getRetirementFund2050());
                        finGoal.setName("Retirement Fund 2050");
                        finGoal.setTargetDate("2049-03-31");
                        finGoal.setTargetValue(1000000);
                        finGoal.setFinalActualValue(15000);
                        finGoal.setType("Retirement");
                        lstFinancialGoals.add(finGoal);
                        lstSampleFinancialGoals.add(finGoal);

                        finGoal = new FinancialGoalCsv();
                        finGoal.setAccountData(demoAccount);
                        finGoal.setActualValue(280000);
                        finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                        finGoal.setId(sampleRecordsConfig.getTahoeVacationHome());
                        finGoal.setName("Tahoe Vacation Home");
                        finGoal.setTargetDate("2021-05-26");
                        finGoal.setTargetValue(450000);
                        finGoal.setFinalActualValue(280000);
                        finGoal.setType("Home Purchase");
                        lstFinancialGoals.add(finGoal);
                        lstSampleFinancialGoals.add(finGoal);
                    }
                    else {
                        int probabilityOfCreatingGoal = Helper.getRandomNumberInRange(1, 100);
                        if (probabilityOfCreatingGoal <= 10) {
                            
                            int targetDays = Helper.getRandomNumberInRange(365, 365*3);
                            Calendar targetCalDate = (Calendar)currentSnapshotDate.clone();

                            int rndCountOfGoals = Helper.getRandomNumberInRange(1, 2);
                            for (int g = 0; g < rndCountOfGoals; g++) {
                                
                                int rndGoalSelector = Helper.getRandomNumberInRange(1, 100);

                                if (rndGoalSelector <= 25) {
                                    // Home Purchase
                                    finGoal = new FinancialGoalCsv();
                                    finGoal.setAccountData(demoAccount);
                                    finGoal.setType("Home Purchase");
                                    finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                                    finGoal.setName(demoAccount.getName() + " Vacation Home");
                                    finGoal.setId(sampleRecordsConfig.getHomePurchaseGoal());
                                    
                                    targetCalDate.add(Calendar.DAY_OF_YEAR, targetDays);
                                    finGoal.setTargetDate(dateFormat.format(targetCalDate.getTime()));
                                    finGoal.setTargetValue(Helper.getRandomNumberInRange(50000, 200000));
                                    finGoal.setActualValue(Helper.getRandomNumberInRange(5000, finGoal.getTargetValue()));                            
                                    lstFinancialGoals.add(finGoal);
                                }
                                else if(rndGoalSelector > 25 && rndGoalSelector <= 50){
                                    // Retirement
                                    finGoal = new FinancialGoalCsv();
                                    finGoal.setAccountData(demoAccount);
                                    finGoal.setType("Retirement");
                                    finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                                    finGoal.setName(demoAccount.getName() + " Retirement");
                                    finGoal.setId(sampleRecordsConfig.getRetirementGoal());                     
                                    targetDays = (70 - demoAccount.getPrimaryContactAge()) * 365;
                                    if (targetDays <= 0) {
                                        targetDays = 365;
                                    }
                                    targetCalDate = (Calendar)currentSnapshotDate.clone();
                                    targetCalDate.add(Calendar.DAY_OF_YEAR, targetDays);
                                    finGoal.setTargetDate(dateFormat.format(targetCalDate.getTime()));
                                    finGoal.setTargetValue(Helper.getRandomNumberInRange(100000, 500000));
                                    finGoal.setActualValue(Helper.getRandomNumberInRange(25000, finGoal.getTargetValue()));                            
                                    lstFinancialGoals.add(finGoal); 
                                }
                                else if(rndGoalSelector > 50 && rndGoalSelector <= 75){
                                    // Education
                                    finGoal = new FinancialGoalCsv();
                                    finGoal.setAccountData(demoAccount);
                                    finGoal.setType("Education");
                                    finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                                    finGoal.setName(demoAccount.getName() + " Education");
                                    finGoal.setId(sampleRecordsConfig.getEducationGoal());
                                    
                                    targetCalDate.add(Calendar.DAY_OF_YEAR, targetDays);
                                    finGoal.setTargetDate(dateFormat.format(targetCalDate.getTime()));
                                    finGoal.setTargetValue(Helper.getRandomNumberInRange(75000, 250000));
                                    finGoal.setActualValue(Helper.getRandomNumberInRange(25000, finGoal.getTargetValue()));
                                    lstFinancialGoals.add(finGoal);
                                }
                                else {
                                    // Other
                                    finGoal = new FinancialGoalCsv();
                                    finGoal.setAccountData(demoAccount);
                                    finGoal.setType("Other");
                                    finGoal.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                                    finGoal.setName(demoAccount.getName() + " Other");
                                    finGoal.setId(sampleRecordsConfig.getOtherGoal());
                                    
                                    targetCalDate.add(Calendar.DAY_OF_YEAR, targetDays);
                                    finGoal.setTargetDate(dateFormat.format(targetCalDate.getTime()));
                                    finGoal.setTargetValue(Helper.getRandomNumberInRange(25000, 150000));
                                    finGoal.setActualValue(Helper.getRandomNumberInRange(5000, finGoal.getTargetValue()));
                                    lstFinancialGoals.add(finGoal);
                                }
                            }                                
                        }
                    }

                    // Financial Goal Owner Data
                    if (finGoal != null) {
                        UserOwnerCsv goalOwner = advisorsMap.get(finGoal.getAccountOwnerName());
                        finGoal.setOwnerData(goalOwner);
                    }
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

                if (weeksCounter == 4) {
                    // Financial Account Transaction snapshots only monthly
                    for (FinancialAccountTransactionCsv trForSnapshot : lstFinAccountTransactions) {
                        genFinAcctTrnSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDates, trForSnapshot.getRowOfData()));
                    }
                }
            
                //cantIterations++; // One more week/iterarion
                //currentSnapshotDate.add(Calendar.WEEK_OF_YEAR, 1); // Step one week to the future
                accountsCreatedCount += accountsToCreateCount;

                if ( (monthsCounter % 2) == 0 && monthsCounter > 0 && (weeksCounter == 4) ) {
                    // Campaings, one every two months
                    System.out.println("Creating campaign in month: " + monthsCounter + " and week: " + weeksCounter);

                    CampaignCsv camp = new CampaignCsv();
                    if (csvCampaignIterator.hasNext()) {
                        CampaignCsv currentCamp = csvCampaignIterator.next();
                        camp.setId(currentCamp.getId());
                        camp.setName(currentCamp.getName());
                    }
                    camp.setStartDate(dateFormat.format(currentSnapshotDate.getTime()));
                    int campNumberSent = Helper.getRandomNumberInRange(MIN_NUMBER_SENT_PER_CAMPAIGN, MAX_NUMBER_SENT_PER_CAMPAIGN);
                    int campNumberOfResp = Helper.getRandomNumberInRange(1, campNumberSent);
                    camp.setNumberSent(campNumberSent);
                    camp.setNumberOfResponses(campNumberOfResp);
                    camp.setIsActive(Math.random() < 0.5);

                    // Campaign Status
                    List<String> lstCampaignStatus = new ArrayList<String>();
                    if (camp.isIsActive()) {
                        Collections.addAll(lstCampaignStatus, "In Progress", "Completed");
                        int rndTwoOpts = Helper.getRandomNumberInRange(0, 1);
                        camp.setStatus(lstCampaignStatus.get(rndTwoOpts));
                    } 
                    else {
                        Collections.addAll(lstCampaignStatus, "Planned", "Aborted");
                        int rndTwoOpts = Helper.getRandomNumberInRange(0, 1);
                        camp.setStatus(lstCampaignStatus.get(rndTwoOpts));
                    }

                    // Owner
                    RandomString rndStringSelected = stringSel.getRandomString();
                    UserOwnerCsv rndOwner = advisorsMap.get(rndStringSelected.getRandomString());
                    camp.setOwnerData(rndOwner);

                    String rndCampaignType = lstCampaignType.get(Helper.getRandomNumberInRange(0, lstCampaignType.size() - 1));
                    camp.setType(rndCampaignType);

                    int campActualCost = Helper.getRandomNumberInRange(MIN_CAMPAIGN_ACTUAL_COST, MAX_CAMPAIGN_ACTUAL_COST);
                    camp.setActualCost(campActualCost);

                    lstCampaigns.add(camp);

                    // Number of Won Opptys based on number of responses
                    int campWonOppties = campNumberOfResp > 1 ? Helper.getRandomNumberInRange(1, campNumberOfResp) : campNumberOfResp;
                    camp.setNumberOfWonOpportunities(campWonOppties);
                    
                    // int campMemberLeadsCount = 0;
                    // int campMembersContactsCount = 0;
                    CampaignMemberCsv currentCampMember;
                    for (int i = 0; i < campNumberSent; i++) {
                        CampaignMemberCsv campMember = new CampaignMemberCsv();
                        
                        if (csvCampMembeIterator.hasNext()) {
                            currentCampMember = csvCampMembeIterator.next();
                            campMember.setId(currentCampMember.getId());
                            campMember.setName(currentCampMember.getName());
                            campMember.setCampaignId(camp.getId());
                        
                            String rndCampaignMemberType = lstCampaignMemberType.get(Helper.getRandomNumberInRange(0, lstCampaignMemberType.size() - 1));
                            campMember.setType(rndCampaignMemberType);
                            campMember.setHasResponded(Math.random() < 0.5);

                            int firstPartPhone = Helper.getRandomNumberInRange(100, 999);
                            int secondPartPhone = Helper.getRandomNumberInRange(100, 999);
                            int thirdPartPhone = firstPartPhone = Helper.getRandomNumberInRange(1000, 9999);
                            String rndPhone = "(" + firstPartPhone + ")-" + secondPartPhone + "-" + thirdPartPhone;

                            // Contact/Lead data
                            if (rndCampaignMemberType.equals("Lead and Referral")) {
                                //campMemberLeadsCount++;
                                campMember.setLeadEmail(campMember.getName().replace(" ", "").replace("(", "").replace(")","").toLowerCase() + "@example.com");
                                campMember.setLeadName(campMember.getName());
                                campMember.setLeadPhone(rndPhone);
                            } 
                            else {
                                //campMembersContactsCount++;
                                campMember.setContactEmail(campMember.getName().replace(" ", "").replace("(", "").replace(")","").toLowerCase() + "@example.com");
                                campMember.setContactMobilePhone(rndPhone);
                                campMember.setContactName(campMember.getName());
                            }

                            campMember.setCampaignData(camp);

                            lstCampaignMembers.add(campMember);
                        }

                    }

                }

                if (weeksCounter == 4) {
                    // We will snapshot the sample financial goals
                    //for (FinancialGoalCsv sampleFinGoal : lstSampleFinancialGoals) {
                    //    genFinGoalSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDates, sampleFinGoal.getRowOfData()));
                    //}
                    monthsCounter++; 
                    weeksCounter = 0;
                    for (FinancialGoalCsv sampleFinGoal : lstFinancialGoals) {
                        genFinGoalSnapCsvWriter.writeNext(Helper.concatArrays(snapshotDates, sampleFinGoal.getRowOfData()));
                    }
                }
                System.out.println("Created: " + accountsToCreateCount + " accounts.");
            }

            genAcctBeanToCsv.write(lstAccounts);
            genFinAcctBeanToCsv.write(lstFinAccounts);
            genFinAcctTrnBeanToCsv.write(lstFinAccountTransactions);
            genActivityBeanToCsv.write(lstActivities);
            genCaseBeanToCsv.write(lstCases);            
            genCampBeanToCsv.write(lstCampaigns);
            genFinGoalsBeanToCsv.write(lstFinancialGoals);
            genCampMemberBeanToCsv.write(lstCampaignMembers);

            System.out.println("Count of weeks: " + lstDatesToProcess.size());
            System.out.println("Total created clients: " + accountsCreatedCount);

            // SECOND PART: Leads & Referrals data

            Iterator<LeadCsv> csvLeadsIterator = leadsCsvToBean.iterator();
            //List<LeadProductInterest> lstLeadProdInterest = new LinkedList<LeadProductInterest>();
            // LeadProductInterest lpi = new LeadProductInterest();
            // lpi.setProductInterestName("Retirement");
            // lpi.setRelativeProbability(60);
            // lstLeadProdInterest.add(lpi);
            // lpi = new LeadProductInterest();
            // lpi.setProductInterestName("Estate Planning");
            // lpi.setRelativeProbability(10);
            // lstLeadProdInterest.add(lpi);
            // lpi = new LeadProductInterest();
            // lpi.setProductInterestName("Investments");
            // lpi.setRelativeProbability(40);
            // lstLeadProdInterest.add(lpi);
            // lpi = new LeadProductInterest();
            // lpi.setProductInterestName("Real-Estate");
            // lpi.setRelativeProbability(10);
            // lstLeadProdInterest.add(lpi);
            // RandomLeadProductInterestSelector rndLpi = new RandomLeadProductInterestSelector(lstLeadProdInterest);

            // Lead Expressed Interest
            ArrayList<String> lstLeadExpressedInterests = new ArrayList<String>();
            Collections.addAll(lstLeadExpressedInterests, 
                "Savings Account",
                "Checking Account",                
                "Day to Day Banking",
                "Manage Money",
                "Property Purchase",
                "Investments",
                "Education",
                "Manage Debt"
            );

            // Lead Expressed Interest
            ArrayList<String> lstLeadRecordTypes = new ArrayList<String>();
            Collections.addAll(lstLeadRecordTypes, 
                "Retirement Planning",
                "General",                
                "Person Referral"
            );

            // Referrer Users
            ArrayList<String> lstLeadReferrerUsers = new ArrayList<String>();
            Collections.addAll(lstLeadReferrerUsers, 
                "Allen Advisor",
                "Mark Garet",
                "Chelsea Advisor",
                "Brenda Banker"
            );

            // Referrer Contacts
            ArrayList<String> lstLeadReferrerContacts = new ArrayList<String>();
            Collections.addAll(lstLeadReferrerContacts, 
                "Ajay Moore",
                "Beatrice Spears",
                "Benjamin Michael",
                "Austin Harvey"
            );

            // Lead Status Sequence for Converted
            ArrayList<String> lstLeadStatusSequenceConverted = new ArrayList<String>();
            Collections.addAll(lstLeadStatusSequenceConverted, 
                "Unqualified",
                "New",
                "Working - Contacted",
                "Nurturing - Contacted",
                "Converted"
            );

            // Lead Status Sequence for Closed - Not Converted
            ArrayList<String> lstLeadStatusSequenceNotConverted = new ArrayList<String>();
            Collections.addAll(lstLeadStatusSequenceNotConverted, 
                "Unqualified",
                "New",
                "Working - Contacted",
                "Nurturing - Contacted",
                "Closed - Not Converted"
            );

            Calendar dateOfLatestCreatedLead = Calendar.getInstance();
            dateOfLatestCreatedLead.setTimeInMillis(0); // Min date possible

            while (csvLeadsIterator.hasNext()) {
                LeadCsv currentLead = csvLeadsIterator.next();
                //currentLead.setProductInterest(rndLpi.getRandomLeadProductInterest().getProductInterestName());
                //Date leadCreatedDate = dateFormat.parse(currentLead.getCreatedDate());
                //Calendar calNow = Calendar.getInstance();
                //Date nowDate = calNow.getTime();
                //currentLead.setLeadAge(Helper.getDaysBetween(leadCreatedDate, nowDate));
                currentLead.setName(currentLead.getFirstName() + " " + currentLead.getLastName());                

                String createdDateStr = currentLead.getCreatedDate();
                Date createdDate = dateFormat.parse(createdDateStr);
                Calendar calCreatedDate = Calendar.getInstance();
                calCreatedDate.setTime(createdDate);

                if (calCreatedDate.compareTo(dateOfLatestCreatedLead) >= 0) {
                    dateOfLatestCreatedLead.setTime(createdDate);
                }
                
                RandomString rndStringSelected = stringSel.getRandomString();
                UserOwnerCsv rndOwner = advisorsMap.get(rndStringSelected.getRandomString());
                currentLead.setOwnerData(rndOwner);

                currentLead.setStartState("Received");
                currentLead.setAnnualRevenue(Helper.getRandomNumberInRange(50000, 1000000));
                currentLead.setEmail(currentLead.getName() + "@example.com");
                
                String rndExpressedInterest = lstLeadExpressedInterests.get(Helper.getRandomNumberInRange(0, lstLeadExpressedInterests.size() - 1));
                currentLead.setExpressedInterest(rndExpressedInterest);

                //(998)-876-4445
                int firstPartPhone = Helper.getRandomNumberInRange(100, 999);
                int secondPartPhone = Helper.getRandomNumberInRange(100, 999);
                int thirdPartPhone = firstPartPhone = Helper.getRandomNumberInRange(1000, 9999);
                currentLead.setPhone("(" + firstPartPhone + ")-" + secondPartPhone + "-" + thirdPartPhone);
                
                int rndReferrerTypeIndex = Helper.getRandomNumberInRange(0, 1);
                String leadReferrer = "";

                if (rndReferrerTypeIndex == 0) {
                    // Will use User
                    String rndReferrerUser = lstLeadReferrerUsers.get(Helper.getRandomNumberInRange(0, lstLeadReferrerUsers.size() - 1));
                    currentLead.setReferredByUser(rndReferrerUser);
                    leadReferrer = rndReferrerUser;
                }
                else {
                    // Will use Contact
                    String rndReferrerContact = lstLeadReferrerContacts.get(Helper.getRandomNumberInRange(0, lstLeadReferrerContacts.size() - 1));
                    currentLead.setReferredByContact(rndReferrerContact);
                    leadReferrer = rndReferrerContact;
                }

                currentLead.setReferrer(leadReferrer);
                
                String rndLeadRT = lstLeadRecordTypes.get(Helper.getRandomNumberInRange(0, lstLeadRecordTypes.size() - 1));
                currentLead.setRecordTypeDeveloperName(rndLeadRT);
                currentLead.setPotentialValue(Helper.getRandomNumberInRange(50000, 750000));

                lstLeads.add(currentLead);
            }            
            
            System.out.println("Date of the latests converted Lead: " + dateFormat.format(dateOfLatestCreatedLead.getTime()));
            long lLeadDaysToShift = Helper.getDaysBetween(dateOfLatestCreatedLead.getTime(), Calendar.getInstance().getTime());
            Long lObjLeadDts = Long.valueOf(lLeadDaysToShift);
            int daysToShiftLeads = lObjLeadDts.intValue();
            System.out.println("Days to shift Lead dates: " + daysToShiftLeads);

            for (LeadCsv leadToShift : lstLeads) {
                Date leadCreatedDate = dateFormat.parse(leadToShift.getCreatedDate());
                Calendar calLeadCreatedDate = Calendar.getInstance();
                calLeadCreatedDate.setTime(leadCreatedDate);
                calLeadCreatedDate.add(Calendar.DATE, daysToShiftLeads);
                Calendar calNow = Calendar.getInstance();
                Date nowDate = calNow.getTime();
                Calendar calHistoryStart = (Calendar)calLeadCreatedDate.clone();
                Calendar calHistoryEnd = null;

                long lDaysSinceCreation = Helper.getDaysBetween(leadCreatedDate, nowDate);
                Long lObjDaysSinceCreation = Long.valueOf(lDaysSinceCreation);
                int daysSinceCreation = lObjDaysSinceCreation.intValue();
                
                leadToShift.setCreatedDate(dateFormat.format(calLeadCreatedDate.getTime()));
                leadToShift.setLeadAge(Helper.getDaysBetween(calLeadCreatedDate.getTime(), nowDate));
                leadToShift.setConverted(false);

                Calendar calLeadConvertedDate = (Calendar) calLeadCreatedDate.clone();
                // Converted Date
                if (leadToShift.getStatus().equals("Converted")) {
                    
                    
                    if (daysSinceCreation > 0) {
                        int daysToConvert = Helper.getRandomNumberInRange(0, daysSinceCreation);
                        
                        calLeadConvertedDate.add(Calendar.DATE, daysToConvert);
                        leadToShift.setConvertedDate(dateFormat.format(calLeadConvertedDate.getTime()));
                        calHistoryEnd = (Calendar)calLeadConvertedDate.clone();
                    } 
                    else {
                        leadToShift.setConvertedDate(dateFormat.format(calLeadCreatedDate.getTime()));
                        calHistoryEnd = (Calendar)calLeadCreatedDate.clone();
                    }
                    
                    leadToShift.setConverted(true);

                    // Converted Opportunity Close Date
                    Calendar calConvOpptyCloseDate = (Calendar) calLeadConvertedDate.clone();
                    int daysToClose = Helper.getRandomNumberInRange(30, 60);
                    calConvOpptyCloseDate.add(Calendar.DAY_OF_MONTH, daysToClose);
                    leadToShift.setConvertedOppCloseDate(dateFormat.format(calConvOpptyCloseDate.getTime()));
                }

                // Last Activity Date
                int daysToLastActivity = Helper.getRandomNumberInRange(0, daysSinceCreation);
                Calendar calLastActivity = (Calendar)calLeadCreatedDate.clone();
                calLastActivity.add(Calendar.DAY_OF_MONTH, daysToLastActivity);
                if (leadToShift.getStatus().equals("Converted")) {
                    // if (calLeadConvertedDate.compareTo(calLastActivity) < 0) {
                    //     calLastActivity = (Calendar)calLeadConvertedDate.clone();
                    // }
                    Date auxConvDate = dateFormat.parse(leadToShift.getConvertedDate());
                    Calendar calAuxConvDate = Calendar.getInstance();
                    calAuxConvDate.setTime(auxConvDate);
                    if (calAuxConvDate.compareTo(calLastActivity) < 0) {
                        calLastActivity = (Calendar)calLeadConvertedDate.clone();
                    }
                }
                String lastActivityDateStr = dateFormat.format(calLastActivity.getTime());
                leadToShift.setDaysSinceLastActivity(daysSinceCreation - daysToLastActivity);
                leadToShift.setLastActivityDate(lastActivityDateStr);
                leadToShift.setLastModifiedDate(lastActivityDateStr);

                if (calHistoryEnd == null) {
                    calHistoryEnd = (Calendar)calLastActivity.clone();
                }

                int activityTouches = Helper.getRandomNumberInRange(3, 10);

                EventCsv leadEvent = new EventCsv();
                leadEvent.setLeadId(leadToShift.getId());
                leadEvent.setLeadData(leadToShift);
                leadEvent.setActivityDate(lastActivityDateStr);

                // Owner data
                RandomString rndStringSelected = stringSel.getRandomString();
                UserOwnerCsv rndOwner = advisorsMap.get(rndStringSelected.getRandomString());
                leadEvent.setOwnerData(rndOwner);
                leadEvent.setTouches(activityTouches);

                lstEvents.add(leadEvent);
                
                leadToShift.setActivityTouches(activityTouches);

                if (leadToShift.isConverted()) {
                    
                    int activityTouchesToConvert = 3;
                    if (activityTouches > 3) {
                        activityTouchesToConvert = Helper.getRandomNumberInRange(3, activityTouches);
                    }
                    
                    leadToShift.setActivityTouchesToConvert(activityTouchesToConvert);
                }
                else {
                    leadToShift.setActivityTouchesToConvert(activityTouches);
                }

                // History for this Lead
                String leadStatus = leadToShift.getStatus(); // Final Status
                ArrayList<String> lstSequenceToUse = null;
                if (leadStatus.equals("Converted")) {
                    lstSequenceToUse = lstLeadStatusSequenceConverted;
                }
                else {
                    lstSequenceToUse = lstLeadStatusSequenceNotConverted;
                }
                int statusIndex = lstSequenceToUse.indexOf(leadStatus); // How many status transitioned?

                List<String> datesOfHistory = new LinkedList<String>();
                datesOfHistory.add(dateFormat.format(calHistoryStart.getTime())); // At least the start
                Calendar iterHistoryDate = (Calendar)calHistoryStart.clone();
                iterHistoryDate.add(Calendar.DAY_OF_MONTH, 1);

                while (iterHistoryDate.compareTo(calHistoryEnd) <= 0) {
                    datesOfHistory.add(dateFormat.format(iterHistoryDate.getTime()));
                    iterHistoryDate.add(Calendar.DAY_OF_MONTH, 1);
                }

                // So now we have the list of dates that the lead existed from
                // creation until conversion or last activity date

                LeadHistoryCsv currentLeadHistory = new LeadHistoryCsv();
                currentLeadHistory.setCreatedDate(datesOfHistory.get(0));
                currentLeadHistory.setField("Status");
                currentLeadHistory.setLeadId(leadToShift.getId());
                currentLeadHistory.setOldValue(lstSequenceToUse.get(0));
                currentLeadHistory.setNewValue(lstSequenceToUse.get(0));
                String prevStatus = currentLeadHistory.getNewValue();
                lstLeadHistory.add(currentLeadHistory); // First initial item

                for (int i = 1; i < statusIndex; i++) {
                    
                    if (i < datesOfHistory.size() - 1) {                         
                        currentLeadHistory = new LeadHistoryCsv();
                        currentLeadHistory.setCreatedDate(datesOfHistory.get(i));
                        currentLeadHistory.setField("Status");
                        currentLeadHistory.setLeadId(leadToShift.getId());
                        currentLeadHistory.setOldValue(prevStatus);
                        currentLeadHistory.setNewValue(lstSequenceToUse.get(i));
                        lstLeadHistory.add(currentLeadHistory);

                        prevStatus = lstSequenceToUse.get(i);
                    }
                }

                currentLeadHistory = new LeadHistoryCsv();
                currentLeadHistory.setCreatedDate(datesOfHistory.get(datesOfHistory.size() - 1));
                currentLeadHistory.setField("Status");
                currentLeadHistory.setLeadId(leadToShift.getId());
                currentLeadHistory.setOldValue(prevStatus);
                currentLeadHistory.setNewValue(lstSequenceToUse.get(statusIndex));

                lstLeadHistory.add(currentLeadHistory); // Last Item
            }

            System.out.println("Count of Leads: " + lstLeads.size());
            genLeadBeanToCsv.write(lstLeads);
            genEventsBeanToCsv.write(lstEvents);
            genLeadHistBeanToCsv.write(lstLeadHistory);
            
            // THIRD PART: Opportunity, Pipeline Trending and Quota data            
            
            Iterator<OpportunityCsv> csvOpptyIterator = opptyCsvToBean.iterator();
            Iterator<PipelineTrendingCsv> csvPipeTrendIterator = pipeTrendCsvToBean.iterator();
            Map<String, OpportunityCsv> opptyMap = new HashMap<String, OpportunityCsv>();
            Map<String, AccountCsv> accountMap = new HashMap<String, AccountCsv>();
            Map<String, UserOwnerCsv> opptyOwnersMap = new HashMap<String, UserOwnerCsv>();
            List<QuotaCsv> lstQuota = new LinkedList<QuotaCsv>();
            List<PipelineTrendingCsv> lstPipelineTrending = new LinkedList<PipelineTrendingCsv>();
            AccountCsv currAccount;
            int activityIndex = 1;
            Calendar dateOfLatestClosedOppty = Calendar.getInstance();
            dateOfLatestClosedOppty.setTimeInMillis(0); // Min date possible
            
            // First we iterate on opportunities
            while (csvOpptyIterator.hasNext()) {
                OpportunityCsv currentOppty = csvOpptyIterator.next();
                String opptyId = currentOppty.getId();
                String accountId = currentOppty.getAccountId();
                
                if (currentOppty.isClosed()) {
                    String closeDateStr = currentOppty.getCloseDate();
                    Date closeDate = dateFormat.parse(closeDateStr);
                    Calendar calCloseDate = Calendar.getInstance();
                    calCloseDate.setTime(closeDate);

                    if (calCloseDate.compareTo(dateOfLatestClosedOppty) >= 0) {
                        dateOfLatestClosedOppty.setTime(closeDate);
                    }
                }                

                // Account exists?
                if (!accountMap.containsKey(accountId)) {
                    currAccount = new AccountCsv();
                    currAccount.setId(accountId);
                    currAccount.setName(currentOppty.getAccountName());
                    currAccount.setCreatedDate(dateFormat.format(currentSnapshotDate.getTime()));
                    
                    String rndMarkSeg = lstMarketingSegments.get(Helper.getRandomNumberInRange(0, lstMarketingSegments.size() - 1));
                    String rndCustSeg = lstCustomerSegments.get(Helper.getRandomNumberInRange(0, lstCustomerSegments.size() - 1));
                    String rndClientCat = lstClientCats.get(Helper.getRandomNumberInRange(0, lstClientCats.size() - 1));
                    
                    currAccount.setMarketingSegment(rndMarkSeg);
                    currAccount.setCustomerSegment(rndCustSeg);
                    currAccount.setClientCategory(rndClientCat);
                    currAccount.setIndustry(currentOppty.getAccountIndustry());
                    accountMap.put(accountId, currAccount);
                }
                else {
                    currAccount = accountMap.get(accountId);
                }

                RandomString rndStringSelected = stringSel.getRandomString();
                UserOwnerCsv rndOpptyOwner = advisorsMap.get(rndStringSelected.getRandomString());

                if (!opptyOwnersMap.containsKey(rndOpptyOwner.getName())) {
                    opptyOwnersMap.put(rndOpptyOwner.getName(), rndOpptyOwner);
                }

                currentOppty.setAccountData(currAccount);
                currentOppty.setOwnerData(rndOpptyOwner);
                currentOppty.setActivityId("Activity " + activityIndex);

                opptyMap.put(opptyId, currentOppty);

                activityIndex++;
            }

            System.out.println("Date of the latests closed oppty: " + dateFormat.format(dateOfLatestClosedOppty.getTime()));
            long lDaysToShift = Helper.getDaysBetween(dateOfLatestClosedOppty.getTime(), Calendar.getInstance().getTime());
            Long lObjDts = Long.valueOf(lDaysToShift);
            int daysToShift = lObjDts.intValue();
            System.out.println("Days to shift dates: " + lDaysToShift);

            for (OpportunityCsv var : opptyMap.values()) {
                String closeDateStr = var.getCloseDate();
                Date closeDate = dateFormat.parse(closeDateStr);
                Calendar calCloseDate = Calendar.getInstance();
                calCloseDate.setTime(closeDate);
                calCloseDate.add(Calendar.DATE, daysToShift);
                var.setCloseDate(dateFormat.format(calCloseDate.getTime()));
                var.setDaysSinceLastActivity(var.getDaysSinceLastActivity() + daysToShift);
                var.setOpportunityAge(var.getOpportunityAge() + daysToShift);

                Calendar calOpptyCreatedDate = Calendar.getInstance();
                calOpptyCreatedDate.add(Calendar.DAY_OF_MONTH, -var.getOpportunityAge());
                var.setCreatedDate(dateFormat.format(calOpptyCreatedDate.getTime()));

                RandomString rndStringSelected = stringSel.getRandomString();
                UserOwnerCsv rndOwner = advisorsMap.get(rndStringSelected.getRandomString());
                var.setOwnerSmallPhotoUrl(rndOwner.getSmallPhotoUrl());
            }

            // Quota file, data for each owner, 3 years quota
            
            for (UserOwnerCsv oppOwner : opptyOwnersMap.values()) {
                
                Calendar quotaStartDate = Calendar.getInstance();
                quotaStartDate.add(Calendar.YEAR, -1); // 1 year to the past
                int currentYear = quotaStartDate.get(Calendar.YEAR);

                for (int yearStep = 0; yearStep <= 2; yearStep++) {
                
                    for (int monthStep = 1; monthStep <= 12; monthStep++) {
                        
                        QuotaCsv quotaItem = new QuotaCsv();
                        quotaItem.setUserOwnerData(oppOwner);
                        quotaStartDate.set(currentYear, monthStep - 1, 1);
                        quotaItem.setStartDate(dateFormat.format(quotaStartDate.getTime()));

                        if (monthStep % 3 == 1) {
                            quotaItem.setQuotaAmount(2500);
                        } 
                        else if(monthStep % 3 == 2){
                            quotaItem.setQuotaAmount(8333);
                        }
                        else {
                            quotaItem.setQuotaAmount(4166);
                        }

                        lstQuota.add(quotaItem);
                    }

                    currentYear = currentYear + 1;
                }
            }

            // Now we iterate on Pipeline Trending, that is, the opportunity historical data

            int pipelineTrendingId = 1;
            while (csvPipeTrendIterator.hasNext()) {
                PipelineTrendingCsv currentOppHist = csvPipeTrendIterator.next();
                String opptyId = currentOppHist.getOpportunityId();

                // Oppty exists?
                if (opptyMap.containsKey(opptyId)) {
                    OpportunityCsv opp = opptyMap.get(opptyId);
                    currentOppHist.setOpportunityData(opp);
                    opp.setRecordTypeName(currentOppHist.getOpportunityRecordTypeName());
                }

                // Timeshifting
                String createdDateStr = currentOppHist.getCreatedDate();
                Date createdDate = dateFormat.parse(createdDateStr);
                Calendar calCreatedDate = Calendar.getInstance();
                calCreatedDate.setTime(createdDate);
                calCreatedDate.add(Calendar.DATE, daysToShift);
                currentOppHist.setCreatedDate(dateFormat.format(calCreatedDate.getTime()));

                String closeDateStr = currentOppHist.getCloseDate();
                Date closeDate = dateFormat.parse(closeDateStr);
                Calendar calCloseDate = Calendar.getInstance();
                calCloseDate.setTime(closeDate);
                calCloseDate.add(Calendar.DATE, daysToShift);
                currentOppHist.setCloseDate(dateFormat.format(calCloseDate.getTime()));
                
                String valFromDateStr = currentOppHist.getValidFromDate();
                Date valFromDate = dateFormat.parse(valFromDateStr);
                Calendar calValFromDDate = Calendar.getInstance();
                calValFromDDate.setTime(valFromDate);
                calValFromDDate.add(Calendar.DATE, daysToShift);
                currentOppHist.setValidFromDate(dateFormat.format(calValFromDDate.getTime()));

                String valToDateStr = currentOppHist.getValidToDate();
                Date valToDate = dateFormat.parse(valToDateStr);
                Calendar calValToDDate = Calendar.getInstance();
                calValToDDate.setTime(valToDate);
                calValToDDate.add(Calendar.DATE, daysToShift);
                currentOppHist.setValidToDate(dateFormat.format(calValToDDate.getTime()));

                currentOppHist.setOpportunityFinancialAccount("N/A");
                currentOppHist.setOpportunityHouseHold("N/A");
                currentOppHist.setId("OppHist-" + pipelineTrendingId);
                pipelineTrendingId++;
                
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