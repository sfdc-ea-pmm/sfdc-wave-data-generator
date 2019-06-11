package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * AccountSnapshot
 */
public class AccountSnapshot {

    @CsvBindByName(column = "SnapshotDate")
    private String snapshotDate;

    private AccountCsv accountData;

    public String getSnapshotDate() {
        return this.snapshotDate;
    }

    public void setSnapshotDate(String snapshotDate) {
        this.snapshotDate = snapshotDate;
    }

    public AccountCsv getAccountData() {
        return this.accountData;
    }

    public void setAccountData(AccountCsv accountData) {
        this.accountData = accountData;
    }

}