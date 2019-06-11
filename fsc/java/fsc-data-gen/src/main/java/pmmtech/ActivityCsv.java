package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * ActivityCsv
 */
public class ActivityCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "AccountId")
    private String accountId;

    @CsvBindByName(column = "AccountName")
    private String accountName;

    @CsvBindByName(column = "AccountRecordTypeName")
    private String accountRecordTypeName;

    @CsvBindByName(column = "ActivityDate")
    private String activityDate;

    @CsvBindByName(column = "Type")
    private String type;

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getAccountId() {
        return this.accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }

    public String getAccountName() {
        return this.accountName;
    }

    public void setAccountName(String accountName) {
        this.accountName = accountName;
    }

    public String getAccountRecordTypeName() {
        return this.accountRecordTypeName;
    }

    public void setAccountRecordTypeName(String accountRecordTypeName) {
        this.accountRecordTypeName = accountRecordTypeName;
    }

    public String getActivityDate() {
        return this.activityDate;
    }

    public void setActivityDate(String activityDate) {
        this.activityDate = activityDate;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

}