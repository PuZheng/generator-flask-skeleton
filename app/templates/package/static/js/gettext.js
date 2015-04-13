define(['i18next', 'locales/translations'], function (i18n, translations) {
    i18n.init({
        fallbackLng: false,
        useCookie: false,
        resStore: translations,
    });
    function gettext() {
        return i18n.t.apply(i18n, arguments);
    }
    return gettext;
});
