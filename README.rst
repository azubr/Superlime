========================================
Superlime plugin for Sublime Text editor
========================================

Superlime requests root/admin rights if a file cannot be saved in SublimeText.

Compatibility
-------------

* Linux (depends on gksudo or kdesudo or pkexec)
* Windows (depends on PowerShell)

* Sublime Text 2
* Sublime Text 3

Mac version of SublimeText supports such functionality natively

|screenshot|

Plugin installation
-------------------

There are two ways to install the plugin:

  * Search for Superlime in `Package Control`_
  * Clone repository_ to SublimeText Packages folder

Possible problems
-----------------
1. On old builds of Sublime Text 3 you could get "unable to create tmp directory" message. In this case set "atomic_save" setting to false. There is no such problem in new builds (tested with build 3065).

.. _Package Control: https://packagecontrol.io/
.. _repository: http://projects.zubr.me/superlime.git
.. |screenshot| image:: http://projects.zubr.me/browser/superlime/screenshot.png?format=raw
