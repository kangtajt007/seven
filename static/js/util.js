/**
 * 替换所有匹配字符
 * @param s1
 * @param s2
 * @returns {string}
 */
String.prototype.replaceAll = function(s1, s2) {
	return this.replace(new RegExp(s1, "gm"), s2);
};