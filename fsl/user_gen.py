import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import datetime


def run(batch_id, source_file_name, output_file_name, source_profiles):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    accounts = data_gen.load_dataset("Profiles", source_profiles, ['Id', 'Name']).dict('Id', 'Name')

    data_gen.add_map_column('Profile.Name', 'ProfileId', accounts)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'FirstName',
        'LastName',
        'Alias',
        'Email',
        'TimeZoneSidKey',
        'Profile.Name',
        'LocaleSidKey',
        'LanguageLocaleKey',
        'EmailEncodingKey',
        'UserPermissionsAvantgoUser',
        'UserPermissionsCallCenterAutoLogin',
        #'UserPermissionsChatterAnswersUser',
        'UserPermissionsInteractionUser',
        #'UserPermissionsJigsawProspectingUser',
        'UserPermissionsKnowledgeUser',
        'UserPermissionsLiveAgentUser',
        'UserPermissionsMarketingUser',
        'UserPermissionsMobileUser',
        'UserPermissionsOfflineUser',
        'UserPermissionsSFContentUser',
        'UserPermissionsSiteforceContributorUser',
        'UserPermissionsSiteforcePublisherUser',
        'UserPermissionsSupportUser',
        'UserPermissionsWorkDotComUserFeature',
        'UserPreferencesActivityRemindersPopup',
        'UserPreferencesApexPagesDeveloperMode',
        'UserPreferencesCacheDiagnostics',
        'UserPreferencesContentEmailAsAndWhen',
        'UserPreferencesContentNoEmail',
        'UserPreferencesDisableAllFeedsEmail',
        'UserPreferencesDisableBookmarkEmail',
        'UserPreferencesDisableChangeCommentEmail',
        'UserPreferencesDisableEndorsementEmail',
        'UserPreferencesDisableFeedbackEmail',
        'UserPreferencesDisableFileShareNotificationsForApi',
        'UserPreferencesDisableFollowersEmail',
        'UserPreferencesDisableLaterCommentEmail',
        'UserPreferencesDisableLikeEmail',
        'UserPreferencesDisableMentionsPostEmail',
        'UserPreferencesDisableMessageEmail',
        'UserPreferencesDisableProfilePostEmail',
        'UserPreferencesDisableRewardEmail',
        'UserPreferencesDisableSharePostEmail',
        'UserPreferencesDisableWorkEmail',
        'UserPreferencesDisCommentAfterLikeEmail',
        'UserPreferencesDisMentionsCommentEmail',
        'UserPreferencesDisProfPostCommentEmail',
        'UserPreferencesEnableAutoSubForFeeds',
        'UserPreferencesEventRemindersCheckboxDefault',
        'UserPreferencesHideBiggerPhotoCallout',
        'UserPreferencesHideChatterOnboardingSplash',
        'UserPreferencesHideCSNDesktopTask',
        'UserPreferencesHideCSNGetChatterMobileTask',
        'UserPreferencesHideEndUserOnboardingAssistantModal',
        'UserPreferencesHideLightningMigrationModal',
        'UserPreferencesHideS1BrowserUI',
        'UserPreferencesHideSecondChatterOnboardingSplash',
        'UserPreferencesHideSfxWelcomeMat',
        #'UserPreferencesJigsawListUser',
        'UserPreferencesLightningExperiencePreferred',
        'UserPreferencesPathAssistantCollapsed',
        'UserPreferencesPreviewLightning',
        'UserPreferencesReminderSoundOff',
        'UserPreferencesShowCityToExternalUsers',
        'UserPreferencesShowCityToGuestUsers',
        'UserPreferencesShowCountryToExternalUsers',
        'UserPreferencesShowCountryToGuestUsers',
        'UserPreferencesShowEmailToExternalUsers',
        'UserPreferencesShowEmailToGuestUsers',
        'UserPreferencesShowFaxToExternalUsers',
        'UserPreferencesShowFaxToGuestUsers',
        'UserPreferencesShowManagerToExternalUsers',
        'UserPreferencesShowManagerToGuestUsers',
        'UserPreferencesShowMobilePhoneToExternalUsers',
        'UserPreferencesShowMobilePhoneToGuestUsers',
        'UserPreferencesShowPostalCodeToExternalUsers',
        'UserPreferencesShowPostalCodeToGuestUsers',
        'UserPreferencesShowProfilePicToGuestUsers',
        'UserPreferencesShowStateToExternalUsers',
        'UserPreferencesShowStateToGuestUsers',
        'UserPreferencesShowStreetAddressToExternalUsers',
        'UserPreferencesShowStreetAddressToGuestUsers',
        'UserPreferencesShowTitleToExternalUsers',
        'UserPreferencesShowTitleToGuestUsers',
        'UserPreferencesShowWorkPhoneToExternalUsers',
        'UserPreferencesShowWorkPhoneToGuestUsers',
        'UserPreferencesSortFeedByComment',
        'UserPreferencesTaskRemindersCheckboxDefault',
        'EmailPreferencesAutoBcc',
        'EmailPreferencesAutoBccStayInTouch',
        'EmailPreferencesStayInTouchReminder',
        'UserPreferencesGlobalNavBarWTShown',
        'UserPreferencesGlobalNavGridMenuWTShown',
        'UserPreferencesCreateLEXAppsWTShown'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/User.csv', 'data/output/User.csv',
        'data/input/Profile.csv')
