[Setup]
AppName=StreamGuard
AppVersion=2.0.0
AppPublisher=StreamGuard Tools
AppPublisherURL=https://github.com/skwasimakram13/StreamGuard
AppSupportURL=https://github.com/skwasimakram13/StreamGuard/issues
AppUpdatesURL=https://github.com/skwasimakram13/StreamGuard/releases
DefaultDirName={autopf}\StreamGuard
DefaultGroupName=StreamGuard
OutputDir=.\InnoSetupOutput
OutputBaseFilename=StreamGuard_Setup_v2.0.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\StreamGuard.exe
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Run `python build.py` first to generate the dist\StreamGuard directory.
Source: "dist\StreamGuard\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\StreamGuard"; Filename: "{app}\StreamGuard.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall StreamGuard"; Filename: "{uninstallexe}"
Name: "{autodesktop}\StreamGuard"; Filename: "{app}\StreamGuard.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\StreamGuard.exe"; Description: "{cm:LaunchProgram,StreamGuard}"; Flags: nowait postinstall skipifsilent

[Code]
var
  KeepConfigPage: TInputOptionWizardPage;

procedure InitializeUninstallProgressForm();
begin
  KeepConfigPage := CreateInputOptionPage(wpWelcome,
    'Configuration Data', 'Do you want to keep your configuration data?',
    'StreamGuard stores encrypted tokens and settings in your AppData directory. ' +
    'If you are reinstalling, keeping data means you will not need to re-authenticate.',
    True, False);

  KeepConfigPage.Add('Keep my configuration data (Recommended if reinstalling)');
  KeepConfigPage.Add('Delete all configuration data (Clean uninstall)');

  KeepConfigPage.Values[0] := True;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  AppDataDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if KeepConfigPage.Values[1] = True then
    begin
      AppDataDir := ExpandConstant('{userappdata}\StreamGuard');
      if DirExists(AppDataDir) then
        DelTree(AppDataDir, True, True, True);
    end;
  end;
end;
