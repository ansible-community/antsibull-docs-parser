# antsibull\-docs\-parser \-\- Python library for processing Ansible documentation markup Release Notes

**Topics**

- <a href="#v1-2-1">v1\.2\.1</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#removed-features-previously-deprecated">Removed Features \(previously deprecated\)</a>
- <a href="#v1-1-1">v1\.1\.1</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#release-summary-3">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v1-0-2">v1\.0\.2</a>
    - <a href="#release-summary-4">Release Summary</a>
    - <a href="#bugfixes-3">Bugfixes</a>
- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#release-summary-5">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#bugfixes-4">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary-6">Release Summary</a>
- <a href="#v0-4-0">v0\.4\.0</a>
    - <a href="#release-summary-7">Release Summary</a>
    - <a href="#minor-changes-3">Minor Changes</a>
    - <a href="#bugfixes-5">Bugfixes</a>
- <a href="#v0-3-0">v0\.3\.0</a>
    - <a href="#release-summary-8">Release Summary</a>
    - <a href="#minor-changes-4">Minor Changes</a>
- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#release-summary-9">Release Summary</a>
    - <a href="#minor-changes-5">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
- <a href="#v0-0-1">v0\.0\.1</a>
    - <a href="#release-summary-10">Release Summary</a>

<a id="v1-2-1"></a>
## v1\.2\.1

<a id="release-summary"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes"></a>
### Bugfixes

* Accept upper\-case letters when validating FQCNs \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/71](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/71)\)\.

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="release-summary-1"></a>
### Release Summary

Maintenance release that drops support for older Python releases\.

<a id="removed-features-previously-deprecated"></a>
### Removed Features \(previously deprecated\)

* antsibull\-docs\-parser no longer supports Python 3\.6\, 3\.7\, and 3\.8\. Python 3\.9\+ is now required \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/68](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/68)\)\.

<a id="v1-1-1"></a>
## v1\.1\.1

<a id="release-summary-2"></a>
### Release Summary

Bugfix release\.

<a id="minor-changes"></a>
### Minor Changes

* Declare support for Python 3\.13 \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/59](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/59)\)\.

<a id="bugfixes-1"></a>
### Bugfixes

* Make sure to also escape pipes \(<code>\\\|</code>\) in reStructured Text \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/65](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/65)\)\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary-3"></a>
### Release Summary

Bugfix and feature release that improves markup parsing and generation with respect to whitespace handling and escaping\.

<a id="minor-changes-1"></a>
### Minor Changes

* Allow to determine how to handle whitespace during parsing with the new <code>whitespace</code> option \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/54](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/54)\)\.
* Always remove some whitespace around <code>HORIZONTALLINE</code> \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/54](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/54)\)\.
* Apply postprocessing to RST and MarkDown to avoid generating invalid markup when input contains whitespace at potentially dangerous places \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/56](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/56)\)\.

<a id="bugfixes-2"></a>
### Bugfixes

* Do not apply URI encoding to visible URL \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/53](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/53)\)\.
* Fix RST escaping to handle other whitespace than spaces correctly \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/56](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/56)\)\.
* Improve handling of empty URL for links \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/53](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/53)\)\.

<a id="v1-0-2"></a>
## v1\.0\.2

<a id="release-summary-4"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-3"></a>
### Bugfixes

* Fix handling of empty markup parameters for RST \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/51](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/51)\)\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="release-summary-5"></a>
### Release Summary

Maintenance release\.

<a id="minor-changes-2"></a>
### Minor Changes

* Declare support for Python 3\.12 \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/45](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/45)\)\.

<a id="bugfixes-4"></a>
### Bugfixes

* Properly escape MarkDown link targets \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/37](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/37)\)\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-6"></a>
### Release Summary

First stable release\. This package is using semantic versioning\, so there will be no more breaking changes until the release of 2\.0\.0\.

<a id="v0-4-0"></a>
## v0\.4\.0

<a id="release-summary-7"></a>
### Release Summary

Feature and bugfix release\.

<a id="minor-changes-3"></a>
### Minor Changes

* Adjust URL escaping to be more similar to JavaScript\'s <code>encodeURI\(\)</code> \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/24](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/24)\)\.
* Also escape <code>\.</code> in MarkDown \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/24](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/24)\)\.

<a id="bugfixes-5"></a>
### Bugfixes

* Fix URL escaping in MarkDown \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/24](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/24)\)\.

<a id="v0-3-0"></a>
## v0\.3\.0

<a id="release-summary-8"></a>
### Release Summary

Feature release\.

<a id="minor-changes-4"></a>
### Minor Changes

* Add support for plain RST rendering \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/20](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/20)\)\.

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="release-summary-9"></a>
### Release Summary

New major release that increases compatibility with the [TypeScript code in antsibull\-docs\-ts](https\://github\.com/ansible\-community/antsibull\-docs\-ts)\.

<a id="minor-changes-5"></a>
### Minor Changes

* Add strict mode for parsing \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/15](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/15)\)\.
* Add support for ansible\-doc like text output \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/17](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/17)\)\.
* Add support for semantic markup in roles \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/9](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/9)\)\.
* Allow to add markup source to every paragraph part \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/18](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/18)\)\.
* Can switch between error messages containing a shortened version of the faulty markup or the full faulty markup command \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/19](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/19)\)\.
* Create script to update/extend the test vectors automatically \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/16](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/16)\)\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* All DOM named tuples now have a <code>source</code> entry before <code>type</code> \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/18](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/18)\)\.
* By default\, the error messages now contain the full faulty markup command \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/19](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/19)\)\.
* Extend <code>OptionNamePart</code> and <code>ReturnValuePart</code> named tuples by adding <code>entrypoint</code> after <code>plugin</code> \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/9](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/9)\)\.
* Modify <code>LinkProvider\.plugin\_option\_like\_link</code> signature to include a new argument <code>entrypoint</code> after <code>plugin</code> \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/9](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/9)\)\.
* <code>CommandParser\.parse</code> has a new <code>source</code> parameter \([https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/18](https\://github\.com/ansible\-community/antsibull\-docs\-parser/pull/18)\)\.

<a id="v0-0-1"></a>
## v0\.0\.1

<a id="release-summary-10"></a>
### Release Summary

Initial experimental release\.
