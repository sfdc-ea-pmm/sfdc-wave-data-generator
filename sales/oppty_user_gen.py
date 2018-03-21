from data_generator import DataGenerator
from data_generator.formula import fake


def run(batch_id, source_file_name, output_file_name, manager_output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = ['Owner.External_Id__c', 'Region__c']
    data_gen.load_source_file(source_file_name, source_columns)

    # rename columns
    data_gen.rename_column('Owner.External_Id__c', 'External_Id__c')
    data_gen.rename_column('Region__c', 'UserRole.Name')

    region_map = {
        'Pacific': 'West Sales',
        "Northwest": 'West Sales',
        "Midwest": 'Central Sales',
        "Southwest": 'Central Sales',
        "Mid-Atlantic": 'Central Sales',
        "Northeast": 'East Sales',
        "Southeast": 'East Sales'
    }
    data_gen.add_map_column('UserRole.Name', 'UserRole.Name', region_map)

    data_gen.apply_transformations()

    # filter out duplicate data
    data_gen.unique()

    # add 3 manager users
    west_manager = ['RVP West', 'W_Sales_User.M.' + str(len(data_gen.rows) + 1)]
    east_manager = ['RVP East', 'W_Sales_User.M.' + str(len(data_gen.rows) + 2)]
    central_manager = ['RVP Central', 'W_Sales_User.M.' + str(len(data_gen.rows) + 3)]

    data_gen.rows.append(west_manager)
    data_gen.rows.append(east_manager)
    data_gen.rows.append(central_manager)

    # generate fake first and last name
    def first_name_formula(column_values):
        id = int(column_values['External_Id__c'].split('.')[-1])
        return fake.first_name_female() if id < 13 else fake.first_name_male()
    data_gen.add_formula_column('FirstName', formula=first_name_formula)
    data_gen.add_formula_column('LastName', formula=fake.last_name)

    # generate data based on fake first and last name
    data_gen.add_formula_column('Name', lambda cv: cv['FirstName'] + ' ' + cv['LastName'])

    def alias_formula(column_values):
        alias = (column_values['FirstName'][0] + column_values['LastName']).lower()
        trimmed_alias = alias[:8] if len(alias) > 8 else alias
        return trimmed_alias
    data_gen.add_formula_column('Alias', formula=alias_formula)
    data_gen.add_formula_column('Email', lambda cv: cv['Alias'] + '@sdodata.ac')

    # generate constant values
    data_gen.add_constant_column('TimeZoneSidKey', 'America/Los_Angeles')
    data_gen.add_constant_column('Profile.Name', 'Standard User')
    data_gen.add_constant_column('LocaleSidKey', 'en_US')
    data_gen.add_constant_column('LanguageLocaleKey', 'en_US')
    data_gen.add_constant_column('EmailEncodingKey', 'ISO-8859-1')
    data_gen.add_constant_column('ForecastEnabled', 'true')

    data_gen.add_constant_column('UserPermissionsAvantgoUser', 'false')
    data_gen.add_constant_column('UserPermissionsCallCenterAutoLogin', 'false')
    data_gen.add_constant_column('UserPermissionsChatterAnswersUser', 'false')
    data_gen.add_constant_column('UserPermissionsInteractionUser', 'false')
    data_gen.add_constant_column('UserPermissionsJigsawProspectingUser', 'false')
    data_gen.add_constant_column('UserPermissionsKnowledgeUser', 'false')
    data_gen.add_constant_column('UserPermissionsLiveAgentUser', 'false')
    data_gen.add_constant_column('UserPermissionsMarketingUser', 'false')
    data_gen.add_constant_column('UserPermissionsMobileUser', 'false')
    data_gen.add_constant_column('UserPermissionsOfflineUser', 'false')
    data_gen.add_constant_column('UserPermissionsSFContentUser', 'false')
    data_gen.add_constant_column('UserPermissionsSiteforceContributorUser', 'false')
    data_gen.add_constant_column('UserPermissionsSiteforcePublisherUser', 'false')
    data_gen.add_constant_column('UserPermissionsSupportUser', 'false')
    data_gen.add_constant_column('UserPermissionsWorkDotComUserFeature', 'false')
    data_gen.add_constant_column('UserPreferencesActivityRemindersPopup', 'false')
    data_gen.add_constant_column('UserPreferencesApexPagesDeveloperMode', 'false')
    data_gen.add_constant_column('UserPreferencesCacheDiagnostics', 'false')
    data_gen.add_constant_column('UserPreferencesContentEmailAsAndWhen', 'false')
    data_gen.add_constant_column('UserPreferencesContentNoEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableAllFeedsEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableBookmarkEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableChangeCommentEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableEndorsementEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableFeedbackEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableFileShareNotificationsForApi', 'false')
    data_gen.add_constant_column('UserPreferencesDisableFollowersEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableLaterCommentEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableLikeEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableMentionsPostEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableMessageEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableProfilePostEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableRewardEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableSharePostEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisableWorkEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisCommentAfterLikeEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisMentionsCommentEmail', 'false')
    data_gen.add_constant_column('UserPreferencesDisProfPostCommentEmail', 'false')
    data_gen.add_constant_column('UserPreferencesEnableAutoSubForFeeds', 'false')
    data_gen.add_constant_column('UserPreferencesEventRemindersCheckboxDefault', 'false')
    data_gen.add_constant_column('UserPreferencesHideBiggerPhotoCallout', 'false')
    data_gen.add_constant_column('UserPreferencesHideChatterOnboardingSplash', 'false')
    data_gen.add_constant_column('UserPreferencesHideCSNDesktopTask', 'false')
    data_gen.add_constant_column('UserPreferencesHideCSNGetChatterMobileTask', 'false')
    data_gen.add_constant_column('UserPreferencesHideEndUserOnboardingAssistantModal', 'false')
    data_gen.add_constant_column('UserPreferencesHideLightningMigrationModal', 'false')
    data_gen.add_constant_column('UserPreferencesHideS1BrowserUI', 'false')
    data_gen.add_constant_column('UserPreferencesHideSecondChatterOnboardingSplash', 'false')
    data_gen.add_constant_column('UserPreferencesHideSfxWelcomeMat', 'false')
    data_gen.add_constant_column('UserPreferencesJigsawListUser', 'false')
    data_gen.add_constant_column('UserPreferencesLightningExperiencePreferred', 'false')
    data_gen.add_constant_column('UserPreferencesPathAssistantCollapsed', 'false')
    data_gen.add_constant_column('UserPreferencesPreviewLightning', 'false')
    data_gen.add_constant_column('UserPreferencesReminderSoundOff', 'false')
    data_gen.add_constant_column('UserPreferencesShowCityToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowCityToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowCountryToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowCountryToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowEmailToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowEmailToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowFaxToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowFaxToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowManagerToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowManagerToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowMobilePhoneToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowMobilePhoneToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowPostalCodeToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowPostalCodeToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowProfilePicToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowStateToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowStateToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowStreetAddressToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowStreetAddressToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowTitleToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowTitleToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowWorkPhoneToExternalUsers', 'false')
    data_gen.add_constant_column('UserPreferencesShowWorkPhoneToGuestUsers', 'false')
    data_gen.add_constant_column('UserPreferencesSortFeedByComment', 'false')
    data_gen.add_constant_column('UserPreferencesTaskRemindersCheckboxDefault', 'false')
    data_gen.add_constant_column('EmailPreferencesAutoBcc', 'false')
    data_gen.add_constant_column('EmailPreferencesAutoBccStayInTouch', 'false')
    data_gen.add_constant_column('EmailPreferencesStayInTouchReminder', 'false')
    data_gen.add_constant_column('UserPreferencesGlobalNavBarWTShown', 'false')
    data_gen.add_constant_column('UserPreferencesGlobalNavGridMenuWTShown', 'false')
    data_gen.add_constant_column('UserPreferencesCreateLEXAppsWTShown', 'false')


    # apply transformations and write file
    data_gen.apply_transformations()
    data_gen.write(output_file_name)

    # create manager file
    data_gen.filter(lambda cv: 'RVP' not in cv['UserRole.Name'])

    manager_map = {
        'West Sales': west_manager[1],
        'East Sales': east_manager[1],
        'Central Sales': central_manager[1],
    }
    data_gen.add_map_column('Manager.External_Id__c', 'UserRole.Name', manager_map)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()
    data_gen.write(manager_output_file_name, ['External_Id__c', 'Manager.External_Id__c'])


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/OpportunityShape.csv', 'data/output/User.csv', 'data/output/Manager.csv')
