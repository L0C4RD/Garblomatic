#!/usr/bin/env python3

##############################################
#
# Garblomatic, v.1.0
# Edmond Locard (@L0C4RD)
# https://github.com/L0C4RD
#
##############################################

import json
import argparse
from enum import IntEnum, unique
from secrets import choice as randomchoice

from urllib.parse import quote
from urllib.request import urlopen
from sys import stdin as STDIN, stdout as STDOUT

class garbler(object):

	languages = {
		"afrikaans" : "af",
		"albanian" : "sq",
		"amharic" : "am",
		"arabic" : "ar",
		"armenian" : "hy",
		"azerbaijani" : "az",
		"basque" : "eu",
		"belarusian" : "be",
		"bengali" : "bn",
		"bosnian" : "bs",
		"bulgarian" : "bg",
		"catalan" : "ca",
		"cebuano" : "ceb",
		"chinese-simp" : "zh-CN",
		"chinese-trad" : "zh-TW",
		"corsican" : "co",
		"croatian" : "hr",
		"czech" : "cs",
		"danish" : "da",
		"dutch" : "nl",
		"english" : "en",
		"esperanto" : "eo",
		"estonian" : "et",
		"finnish" : "fi",
		"french" : "fr",
		"frisian" : "fy",
		"galician" : "gl",
		"georgian" : "ka",
		"german" : "de",
		"greek" : "el",
		"gujarati" : "gu",
		"haitian-creole" : "ht",
		"hausa" : "ha",
		"hawaiian" : "haw",
		"hebrew" : "he",
		"hindi" : "hi",
		"hmong" : "hmn",
		"hungarian" : "hu",
		"icelandic" : "is",
		"igbo" : "ig",
		"indonesian" : "id",
		"irish" : "ga",
		"italian" : "it",
		"japanese" : "ja",
		"javanese" : "jv",
		"kannada" : "kn",
		"kazakh" : "kk",
		"khmer" : "km",
		"kinyarwanda" : "rw",
		"korean" : "ko",
		"kurdish" : "ku",
		"kyrgyz" : "ky",
		"lao" : "lo",
		"latin" : "la",
		"latvian" : "lv",
		"lithuanian" : "lt",
		"luxembourgish" : "lb",
		"macedonian" : "mk",
		"malagasy" : "mg",
		"malay" : "ms",
		"malayalam" : "ml",
		"maltese" : "mt",
		"maori" : "mi",
		"marathi" : "mr",
		"mongolian" : "mn",
		"myanmar" : "my",
		"burmese" : "my",
		"nepali" : "ne",
		"norwegian" : "no",
		"nyanja" : "ny",
		"chichewa" : "ny",
		"odia" : "or",
		"oriya" : "or",
		"pashto" : "ps",
		"persian" : "fa",
		"polish" : "pl",
		"portuguese" : "pt",
		"punjabi" : "pa",
		"romanian" : "ro",
		"russian" : "ru",
		"samoan" : "sm",
		"scots-gaelic" : "gd",
		"serbian" : "sr",
		"sesotho" : "st",
		"shona" : "sn",
		"sindhi" : "sd",
		"sinhala" : "si",
		"sinhalese" : "si",
		"slovak" : "sk",
		"slovenian" : "sl",
		"somali" : "so",
		"spanish" : "es",
		"sundanese" : "su",
		"swahili" : "sw",
		"swedish" : "sv",
		"tagalog" : "tl",
		"filipino" : "tl",
		"tajik" : "tg",
		"tamil" : "ta",
		"tatar" : "tt",
		"telugu" : "te",
		"thai" : "th",
		"turkish" : "tr",
		"turkmen" : "tk",
		"ukrainian" : "uk",
		"urdu" : "ur",
		"uyghur" : "ug",
		"uzbek" : "uz",
		"vietnamese" : "vi",
		"welsh" : "cy",
		"xhosa" : "xh",
		"yiddish" : "yi",
		"yoruba" : "yo",
		"zulu" : "zu",
	}
	
	@unique
	class RETURN(IntEnum):
		OK = 0
		BAD_ARGS = -1
		IOERROR = -2
		UNKNOWN_LANG = -3
		API_ERROR = -4

	def call_translate_api(self, source_lang:str, target_lang:str, source_text:str) -> str :

		try:
			uri = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q=" + quote(source_text)
		except:
			raise Exception("Could not format request string for Google API.")

		try:
			r = urlopen(uri)
		except Exception as e:
			raise Exception(f"Could not fetch translation from Google API: {str(e)}")

		try:
			response = json.load(r)
			response_fragments = response[0]
			translated_text = ""
			for fragment in response_fragments:
				translated_text += fragment[0]
		except:
			raise Exception("Could not understand the response from Google API")
		else:
			return translated_text

	def main(self, args):

		#Check for list behaviour first.
		if args.list_langs:
			self.do_list()
			return self.RETURN.OK

		#If specified, check base language.
		base_lang = args.base_lang.lower()
		if base_lang not in self.languages:
			print(f"Unknown language \"{args.base_lang}\"")
			return self.RETURN.UNKNOWN_LANG

		#Otherwise: we're garbling.
		#Check if we have:
		# - s flag
		# - file
		# - neither
		# - both
		if args.stdin and args.file_in:
			print("Please specify either a file from which to read, or the -s flag (but not both)")
			return self.RETURN.BAD_ARGS

		elif args.stdin:
			try:
				source_text = STDIN.read().strip()
			except:
				print("Could not read from stdin.")
				return self.RETURN.IOERROR

		elif args.file_in:
			try:
				with open(args.file_in, "r") as f:
					source_text = f.read().strip()
			except:
				print(f"Could not read from file {args.file_in}")
				return self.RETURN.IOERROR
		
		else: #(Neither specified)
			print("Please specify either a file from which to read, or the -s flag")
			return self.RETURN.BAD_ARGS

		#Check garble settings:
		# - r
		# - langs
		# - neither
		# - both
		if args.languages and (args.num_random_langs is not None):
			print("Please specify either a lsit of languages with which to garble, or the -r flag (but not both)")
			return self.RETURN.BAD_ARGS
		elif args.languages:

			garble_langs = []
			bad_langs = False
			
			for l in args.languages:
				try:
					assert(len(l) >= 2)
					lang_key = l.lower()
					assert(lang_key in self.languages)
				except:
					print(f"Unknown language \"{l}\"")
					bad_langs = True
				else:
					garble_langs.append(lang_key)
			
			if bad_langs:
				return self.RETURN.UNKNOWN_LANG

		elif args.num_random_langs is not None:
			
			if args.num_random_langs < 0:
				print("Please specify a non-negative integer number of languages through which to garble")
				return self.RETURN.BAD_ARGS
			else:
				garble_langs = self.get_random_languages(args.num_random_langs)

		else:
			garble_langs = self.get_random_languages(3)

		#Check output.
		#If it's a file, make sure we can write to it.
		if args.file_out:
			
			try:
				out_file = self.__safe_open__(args.file_out, "w")
			except:
				print(f"Could not open {args.file_out} for writing.")
				return self.RETURN.IOERROR
		else:
			out_file = STDOUT

		#We have everything we need. Do the garble:
		try:
			garbled_text = self.do_garble(source_text, garble_langs, first_lang=base_lang)
		except Exception as e:
			print(f"API error: {str(e)}")
			return self.RETURN.API_ERROR

		#Write out.
		try:
			out_file.write(garbled_text+"\n")
		except Exception as e:
			print (e)
			if args.file_out:
				print(f"Could not write to {args.file_out}")
			else:
				print(f"Could not write to stdout")
			return self.RETURN.IOERROR
			
		#All done.
		return self.RETURN.OK

	def do_list(self):
		for l in self.languages:
			print(l)

	def __init__(self):
		self.closefiles = set()

	def __del__(self):
		for f in self.closefiles:
			try:
				f.close()
			except:
				pass
	
	def __safe_open__(self, path, flags):
		f = open(path, flags)
		self.closefiles.add(f)
		return f

	def get_random_languages(self, num):

		rand_langs = []

		if num > 0:

			langs_as_list = list(self.languages.keys())
			rand_langs.append(randomchoice(langs_as_list))
			
			if len(langs_as_list) > 1:
				while len(rand_langs) < num:	
					next_lang = randomchoice(langs_as_list)
					if self.languages[next_lang] != self.languages[rand_langs[-1]]:
						rand_langs.append(next_lang)

		return rand_langs

	def do_garble(self, source_text:str, lang_chain:list, first_lang="English") -> str:

		#Don't bother if one or both are missing.
		if (not lang_chain) or (not source_text):
			return source_text
		
		original_lang = first_lang
		
		to_lang = first_lang
		updated_text = source_text
		
		for next_lang in lang_chain:
			
			from_lang = to_lang
			to_lang = next_lang
			
			updated_text = self.call_translate_api(
				self.languages[from_lang],
				self.languages[to_lang],
				updated_text
			)
		
		updated_text = self.call_translate_api(
			self.languages[lang_chain[-1]],
			self.languages[original_lang],
			updated_text
		)
		
		return updated_text


if __name__ == "__main__":

	parser = argparse.ArgumentParser(
		description='Garble some text.',
		epilog="For example: garble lol",
	)

	parser.add_argument(
		"file_in", 
		nargs='?', 
		type=str,
		default=None,
		help="path to file to be translated",
		metavar="file",
	)
	parser.add_argument(
		"-s",
		dest="stdin",
		required=False,
		action='store_true',
		default=False,
		help="read from stdin instead of a file",
	)
	parser.add_argument(
		"-l",
		dest="list_langs",
		required=False,
		action='store_true',
		default=False,
		help="List supported languages (no translation is performed)",
	)
	parser.add_argument(
		"-r", "-R",
		dest="num_random_langs",
		required=False,
		default=None,
		type=int,
		help="Select N random languages to garble through.",
		metavar="N"
	)
	parser.add_argument(
		"-o",
		dest="file_out",
		required=False,
		type=str,
		help="Output to a file instead of stdout",
		metavar="path",
		default = None,
	)
	parser.add_argument(
		"-b",
		dest="base_lang",
		required=False,
		default="english",
		type=str,
		help="Specify original language of file to garble. By default, this is English",
		metavar="base_lang",
	)
	parser.add_argument(
		"languages", 
		nargs=argparse.REMAINDER, 
		type=str,
		default=None,
		help="Languages to translate through. If none are specified, three randomly-selected languages are used (as if -r 3 had been specified)",
		metavar="...",
	)

	args = parser.parse_args()

	G = garbler()
	G.main(args)

	exit()
