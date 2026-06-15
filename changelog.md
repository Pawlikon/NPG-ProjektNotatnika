# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- (#10) Małe poprawki w kodzie:
  - Dodano date modyfikacji notatki

  - Ze względu na problemy z branchem mail-handling manualnie przepisałem tu kod na obsługe wysyłki maili

  Mam nadzieje, że nic wiecej tu nie zepsulem xd


- (#9) Complete tag system, documentation:
    - Tags are stored in a global set unique to each notebook to prevent duplicates
    - Global tags are saved into a separate JSON file (`tagi.json`)
    - Input is automatically formatted (whitespace stripped, capitalized) to avoid near-duplicate tags (e.g., "work" vs "Work")
    - Tags can only be added to a note if they exist in the global set (so basically you can add tags to notes only from the list)
    - Tags cannot be duplicated
    - Tags can be removed from note and notebook
    - Removing a tag from the notebook automatically strips it from all existing notes.


- (#8) Classes for notes and notebooks.

### Changed

- (#14) Sprawdzenie czy notatki rzeczywiście się zmieniły
### Removed
