"use strict";
exports.__esModule = true;
/**
 * Convert a date to a relative time string, such as
 * "a minute ago", "in 2 hours", "yesterday", "3 months ago", etc.
 * using Intl.RelativeTimeFormat
 */
function getRelativeTimeString(date, lang) {
    if (lang === void 0) { lang = navigator.language; }
    // Allow dates or times to be passed
    var timeMs = typeof date === "number" ? date : date.getTime();
    // Get the amount of seconds between the given date and now
    var deltaSeconds = Math.round((timeMs - Date.now()) / 1000);
    // Array reprsenting one minute, hour, day, week, month, etc in seconds
    var cutoffs = [60, 3600, 86400, 86400 * 7, 86400 * 30, 86400 * 365, Infinity];
    // Array equivalent to the above but in the string representation of the units
    var units = ["second", "minute", "hour", "day", "week", "month", "year"];
    // Grab the ideal cutoff unit
    var unitIndex = cutoffs.findIndex(function (cutoff) { return cutoff > Math.abs(deltaSeconds); });
    // Get the divisor to divide from the seconds. E.g. if our unit is "day" our divisor
    // is one day in seconds, so we can divide our seconds by this to get the # of days
    var divisor = unitIndex ? cutoffs[unitIndex - 1] : 1;
    // Intl.RelativeTimeFormat do its magic
    var rtf = new Intl.RelativeTimeFormat(lang, { numeric: "auto" });
    return rtf.format(Math.floor(deltaSeconds / divisor), units[unitIndex]);
}
exports.getRelativeTimeString = getRelativeTimeString;
