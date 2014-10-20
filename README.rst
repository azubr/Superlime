========================================
Superlime plugin for Sublime Text editor
========================================

Superlime requests root/admin rights if a file cannot be saved in SublimeText.

Compatibility
-------------

* Linux (depends on gksudo or kdesudo or pkexec)
* Windows (depends on PowerShell)

* Sublime Text 2
* Sublime Text 3 (with "atomic save" switched off)

Mac version of SublimeText supports such functionality natively

|screenshot|

Plugin installation
-------------------

1. There are two ways to install the plugin:

  * Search for Superlime in `Package Control`_
  * Clone repository_ to SublimeText Packages folder

2. Set "atomic_save" setting to false in Sublime Text 3

.. _Package Control: https://sublime.wbond.net/
.. _repository: http://projects.zubr.me/superlime.git
.. |screenshot| image:: http://projects.zubr.me/browser/superlime/screenshot.png?format=raw
