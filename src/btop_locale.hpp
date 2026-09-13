/* Copyright 2021 Aristocratos (jakob@qvantnet.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

	   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

indent = tab
tab-size = 4
*/

#pragma once

#include <string>
#include <string_view>
#include <vector>

//* Internationalization / Localization support for btop++
//* 简体中文汉化：以英文原文为 key 的翻译映射表
namespace Locale {

	//* Initialize the locale system and load translations for the given language code ("en", "zh")
	bool init(const std::string& lang);

	//* Get translated string for key. Returns a value (not a reference) so that
	//* passing a temporary as key is safe, and falls back to the key (English)
	//* when no translation exists.
	std::string get(const std::string& key);

	//* 判断是否存在该 key 的译文（用于「有译文才替换」的场景）
	bool has(const std::string& key);

	//* Get the current language code
	const std::string& currentLanguage();

	//* List available language codes
	std::vector<std::string> availableLanguages();

	//* Reload translations (e.g. after a config change)
	bool reload();

}
