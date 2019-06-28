package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * LeadHistoryCsv
 */
public class LeadHistoryCsv {

    @CsvBindByName(column = "LeadId")
    private String leadId;

    @CsvBindByName(column = "CreatedDate")
    private String createdDate;

    @CsvBindByName(column = "Field")
    private String field;

    @CsvBindByName(column = "NewValue")
    private String newValue;

    @CsvBindByName(column = "OldValue")
    private String oldValue;

    public String getLeadId() {
        return this.leadId;
    }

    public void setLeadId(String leadId) {
        this.leadId = leadId;
    }

    public String getCreatedDate() {
        return this.createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
    }

    public String getField() {
        return this.field;
    }

    public void setField(String field) {
        this.field = field;
    }

    public String getNewValue() {
        return this.newValue;
    }

    public void setNewValue(String newValue) {
        this.newValue = newValue;
    }

    public String getOldValue() {
        return this.oldValue;
    }

    public void setOldValue(String oldValue) {
        this.oldValue = oldValue;
    }

}