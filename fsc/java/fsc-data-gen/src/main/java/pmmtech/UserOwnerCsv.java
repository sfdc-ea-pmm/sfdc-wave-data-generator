package pmmtech;

import com.opencsv.bean.CsvBindByName;

/**
 * UserOwnerCsv
 */
public class UserOwnerCsv {

    @CsvBindByName(column = "Id")
    private String id;

    @CsvBindByName(column = "Name")
    private String name;

    @CsvBindByName(column = "RoleName")
    private String roleName;

    @CsvBindByName(column = "Email")
    private String email;

    @CsvBindByName(column = "State")
    private String state;

    @CsvBindByName(column = "City")
    private String city;

    @CsvBindByName(column = "SmallPhotoUrl")
    private String smallPhotoUrl;

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getState() {
        return this.state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getCity() {
        return this.city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getSmallPhotoUrl() {
        return this.smallPhotoUrl;
    }

    public void setSmallPhotoUrl(String smallPhotoUrl) {
        this.smallPhotoUrl = smallPhotoUrl;
    }

    public String getRoleName() {
        return this.roleName;
    }

    public void setRoleName(String roleName) {
        this.roleName = roleName;
    }

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

}