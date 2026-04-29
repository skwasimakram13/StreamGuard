#ifndef ReleaseDir
#define ReleaseDir "build\windows\runner\Release"
#endif

[Setup]
AppName=StreamGuard
AppVersion=2.1.1
AppPublisher=StreamGuard Tools
AppPublisherURL=https://github.com/skwasimakram13/StreamGuard
AppSupportURL=https://github.com/skwasimakram13/StreamGuard/issues
AppUpdatesURL=https://github.com/skwasimakram13/StreamGuard/releases
DefaultDirName={autopf}\StreamGuard
DefaultGroupName=StreamGuard
OutputDir=.\InnoSetupOutput
OutputBaseFilename=StreamGuard_Setup_v2.1.1
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\StreamGuard.exe
MinVersion=10.0
; Always show destination directory and start menu group pages
DisableDirPage=no
DisableProgramGroupPage=no
DisableWelcomePage=no
LicenseFile=LICENSE

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; flet build windows outputs a directory containing the exe and dependencies
Source: "{#ReleaseDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\StreamGuard"; Filename: "{app}\StreamGuard.exe"
Name: "{group}\Uninstall StreamGuard"; Filename: "{uninstallexe}"
Name: "{autodesktop}\StreamGuard"; Filename: "{app}\StreamGuard.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\StreamGuard.exe"; Description: "{cm:LaunchProgram,StreamGuard}"; Flags: nowait postinstall skipifsilent

[Code]
var
  DeleteConfigData: Boolean;

function InitializeUninstall(): Boolean;
begin
  if MsgBox('Do you want to completely delete your configuration data (encrypted tokens and settings)?' + #13#10#13#10 + 'Choose No if you plan to reinstall StreamGuard later.', mbConfirmation, MB_YESNO) = idYes then
    DeleteConfigData := True
  else
    DeleteConfigData := False;
    
  Result := True;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  AppDataDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if DeleteConfigData then
    begin
      AppDataDir := ExpandConstant('{userappdata}\StreamGuard');
      if DirExists(AppDataDir) then
        DelTree(AppDataDir, True, True, True);
    end;
  end;
end;
