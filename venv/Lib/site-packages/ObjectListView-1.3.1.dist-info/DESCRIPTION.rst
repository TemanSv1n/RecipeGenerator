ObjectListView
==============

An ObjectListView is a wrapper around the wx.ListCtrl that makes the
list control easier to use. It also provides some useful extra functionality.

* Automatically transforms a collection of model objects into a fully functional wx.ListCtrl.
* Automatically sorts rows.
* Easily edit the cell values.
* Supports all ListCtrl views (report, list, large and small icons).
* Columns can be fixed-width, have a minimum and/or maximum width, or be space-filling
* Displays a "list is empty" message  when the list is empty (obviously).
* Supports checkboxes in any column.
* Supports alternate rows background colors.
* Supports custom formatting of rows .
* Supports searching (by typing) on any column, even on massive lists.
* Supports custom sorting
* Supports filtering and batched updates
* The ``FastObjectListView`` version can build a list of 10,000 objects in less than 0.1 seconds.
* The ``VirtualObjectListView`` version supports millions of rows through ListCtrl's virtual mode.
* The ``GroupListView`` version supports arranging rows into collapsible groups.
* Effortlessly produce professional-looking reports using a ``ListCtrlPrinter``.

Seriously, after using an ObjectListView, you will never go back to using a plain wx.ListCtrl.


Dependancies
============

  * Python 2.7+
  * wxPython 2.8+



