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
						.replace("with BOM", "_sig") \
						.lower()
			try:
				encoded = content.replace('\n', self.lineEndings[view.line_endings()]).encode(encoding) if encoding != "Hexadecimal" else binascii.unhexlify(string.replace(" ",""))
				tempFile.write(encoded)
			finally:
				tempFile.close()

			#print view.file_name(), ": Saved temp file with encoding " + encoding

			oldScratch = view.is_scratch()
			view.set_scratch(True)
			if 0 == self.copyFile(tempFile.name, view.file_name()):
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
			runasCommand = 'try {$proc = Start-Process \\"$env:COMSPEC\\" \\"/c,%s\\" -verb RunAs -WindowStyle Hidden -WorkingDirectory \\"$env:windir\\" -PassThru; $proc.WaitForExit(); exit $proc.ExitCode } catch {exit 1}' % command
			psCommand = 'powershell -command "%s"' % runasCommand
			return subprocess.call(psCommand, shell=True)
		if os.name == "posix":
			def trySudo(sudo):
				dd="dd if=%s of=%s" % (source, target)
				return subprocess.call(sudo % dd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
			sudoErr = trySudo("pkexec %s")
			if sudoErr == 127:
				sudoErr = trySudo("gksudo %s")
				if sudoErr == 127:
					sudoErr = trySudo("kdesudo %s")
					if sudoErr == 127:
						sudoErr = trySudo("""/usr/bin/osascript -e 'do shell script "%s" with administrator privileges'""")
						if sudoErr:
							sublime.message_dialog("No sudo GUI found")
			return sudoErr
