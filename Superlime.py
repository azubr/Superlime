# Superlime - Requests root/admin rights if a file cannot be saved in SublimeText
# Copyright (C) 2013 Alexey Zubritsky

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sublime, sublime_plugin, subprocess, os, tempfile, re, binascii

class Superlime(sublime_plugin.EventListener):
	lineEndings = {'Windows': '\r\n', 'Unix': '\n', 'CR': '\r'}
	hadSavingError = False

	def on_activated(self, view):
		hadSavingError = self.hadSavingError
		self.hadSavingError = False
		if hadSavingError and sublime.ok_cancel_dialog("Do you want to save file as %s?" % (self.getAdminName()), "Yes"):
			content = view.substr(sublime.Region(0, view.size()))
			tempFile = tempfile.NamedTemporaryFile(delete=False)
			encoding = view.encoding()
			encoding = re.sub(r'.*\((.*)\)', r'\1', encoding) \
						.replace("Windows ", "cp") \
						.replace("cp ", "cp") \
						.replace("ISO ", "iso-") \
						.replace("Mac ", "mac") \
						.replace("KOI8-", "koi8_") \
						.replace("UTF-16 ", "utf_16_") \
						.replace("UTF-8 ", "utf_8") \
						.lower()
			try:
				encoded = content.replace('\n', self.lineEndings[view.line_endings()]).encode(encoding) if encoding != "Hexadecimal" else binascii.unhexlify(string.replace(" ",""))
				tempFile.write(encoded)
			finally:
				tempFile.close()

			#print view.file_name(), ": Saved temp file with encoding " + encoding

			oldScratch = view.is_scratch()
			view.set_scratch(True)
			self.copyFile(tempFile.name, view.file_name())
			view.run_command('revert')
			sublime.set_timeout(lambda: view.set_scratch(oldScratch), 50)
			os.remove(tempFile.name)

	def on_post_save(self, view):
		self.hadSavingError = view.is_dirty()

	def getAdminName(self):
		if os.name == "nt":
			return "administrator"
		else:
			return "root"

	def copyFile(self, source, target):
		if os.name == "nt":
			command = 'copy /y `\\"%s`\\" `\\"%s`\\"' % (source, target)
			runasCommand = 'start-process \\"$env:windir\system32\cmd.exe\\" \\"/c,%s\\" -verb RunAs -WorkingDirectory $env:windir' % command
			psCommand = 'powershell -command "%s"' % runasCommand
			os.system(psCommand)
		if os.name == "posix":
			trySudo = lambda sudo: subprocess.call('%s dd if=%s of=%s' % (sudo, source, target), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
			if trySudo("gksudo") == 127:
				if trySudo("kdesudo"):
					sublime.message_dialog("No sudo GUI found")


			

