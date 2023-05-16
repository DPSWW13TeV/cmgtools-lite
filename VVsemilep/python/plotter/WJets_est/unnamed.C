// Mainframe macro generated from application: python
// By ROOT version 6.14/09 on 2023-05-03 16:41:40

#ifndef ROOT_TGFrame
#include "TGFrame.h"
#endif
#ifndef ROOT_TGListBox
#include "TGListBox.h"
#endif
#ifndef ROOT_TGScrollBar
#include "TGScrollBar.h"
#endif
#ifndef ROOT_TGComboBox
#include "TGComboBox.h"
#endif
#ifndef ROOT_TGMenu
#include "TGMenu.h"
#endif
#ifndef ROOT_TGFileDialog
#include "TGFileDialog.h"
#endif
#ifndef ROOT_TGButtonGroup
#include "TGButtonGroup.h"
#endif
#ifndef ROOT_TGCanvas
#include "TGCanvas.h"
#endif
#ifndef ROOT_TGFSContainer
#include "TGFSContainer.h"
#endif
#ifndef ROOT_TGButton
#include "TGButton.h"
#endif
#ifndef ROOT_TRootContextMenu
#include "TRootContextMenu.h"
#endif
#ifndef ROOT_TGFSComboBox
#include "TGFSComboBox.h"
#endif
#ifndef ROOT_TGLabel
#include "TGLabel.h"
#endif
#ifndef ROOT_TGListView
#include "TGListView.h"
#endif
#ifndef ROOT_TGSplitter
#include "TGSplitter.h"
#endif
#ifndef ROOT_TGTextEntry
#include "TGTextEntry.h"
#endif
#ifndef ROOT_TRootCanvas
#include "TRootCanvas.h"
#endif
#ifndef ROOT_TGDockableFrame
#include "TGDockableFrame.h"
#endif
#ifndef ROOT_TG3DLine
#include "TG3DLine.h"
#endif
#ifndef ROOT_TGToolTip
#include "TGToolTip.h"
#endif

#include "Riostream.h"

void unnamed()
{

   // main frame
   TGMainFrame *fRootCanvas660 = new TGMainFrame(gClient->GetRoot(),10,10,kMainFrame | kVerticalFrame);

   // menu bar
   TGMenuBar *fMenuBar670 = new TGMenuBar(fRootCanvas660,800,22,kHorizontalFrame);

   // "File" menu
   TGPopupMenu *fPopupMenu662 = new TGPopupMenu(gClient->GetDefaultRoot(),110,144,kOwnBackground);
   fPopupMenu662->AddEntry("&New Canvas",0);
   fPopupMenu662->AddEntry("&Open...",1);
   fPopupMenu662->AddEntry("&Close Canvas",13);
   fPopupMenu662->AddSeparator();

   // cascaded menu "Save"
   TGPopupMenu *fPopupMenu661 = new TGPopupMenu(gClient->GetDefaultRoot(),239,168,kOwnBackground);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&ps",5);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&eps",6);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.p&df",7);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&tex",11);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&gif",8);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&jpg",9);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&png",10);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&C",4);
   fPopupMenu661->AddEntry("frame_rrv_mass_lvj_34cefd90.&root",3);
   fPopupMenu662->AddPopup("&Save",fPopupMenu661);
   fPopupMenu662->AddEntry("Save &As...",2);
   fPopupMenu662->AddSeparator();
   fPopupMenu662->AddEntry("&Print...",12);
   fPopupMenu662->AddSeparator();
   fPopupMenu662->AddEntry("&Quit ROOT",14);
   fMenuBar670->AddPopup("&File",fPopupMenu662, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Edit" menu
   TGPopupMenu *fPopupMenu664 = new TGPopupMenu(gClient->GetDefaultRoot(),74,144,kOwnBackground);
   fPopupMenu664->AddEntry("&Style...",15);
   fPopupMenu664->AddSeparator();
   fPopupMenu664->AddEntry("Cu&t",16);
   fPopupMenu664->DisableEntry(16);
   fPopupMenu664->AddEntry("&Copy",17);
   fPopupMenu664->DisableEntry(17);
   fPopupMenu664->AddEntry("&Paste",18);
   fPopupMenu664->DisableEntry(18);
   fPopupMenu664->AddSeparator();

   // cascaded menu "Clear"
   TGPopupMenu *fPopupMenu663 = new TGPopupMenu(gClient->GetDefaultRoot(),74,42,kOwnBackground);
   fPopupMenu663->AddEntry("&Pad",19);
   fPopupMenu663->AddEntry("&Canvas",20);
   fPopupMenu664->AddPopup("C&lear",fPopupMenu663);
   fPopupMenu664->AddSeparator();
   fPopupMenu664->AddEntry("&Undo",21);
   fPopupMenu664->DisableEntry(21);
   fPopupMenu664->AddEntry("&Redo",22);
   fPopupMenu664->DisableEntry(22);
   fMenuBar670->AddPopup("&Edit",fPopupMenu664, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "View" menu
   TGPopupMenu *fPopupMenu666 = new TGPopupMenu(gClient->GetDefaultRoot(),128,180,kOwnBackground);
   fPopupMenu666->AddEntry("&Editor",23);
   fPopupMenu666->AddEntry("&Toolbar",24);
   fPopupMenu666->AddEntry("Event &Statusbar",25);
   fPopupMenu666->AddEntry("T&oolTip Info",26);
   fPopupMenu666->AddSeparator();
   fPopupMenu666->AddEntry("&Colors",27);
   fPopupMenu666->AddEntry("&Fonts",28);
   fPopupMenu666->DisableEntry(28);
   fPopupMenu666->AddEntry("&Markers",29);
   fPopupMenu666->AddSeparator();
   fPopupMenu666->AddEntry("&Iconify",30);
   fPopupMenu666->AddSeparator();

   // cascaded menu "View With"
   TGPopupMenu *fPopupMenu665 = new TGPopupMenu(gClient->GetDefaultRoot(),78,42,kOwnBackground);
   fPopupMenu665->AddEntry("&X3D",31);
   fPopupMenu665->AddEntry("&OpenGL",32);
   fPopupMenu666->AddPopup("&View With",fPopupMenu665);
   fMenuBar670->AddPopup("&View",fPopupMenu666, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Options" menu
   TGPopupMenu *fPopupMenu667 = new TGPopupMenu(gClient->GetDefaultRoot(),151,216,kOwnBackground);
   fPopupMenu667->AddEntry("&Auto Resize Canvas",33);
   fPopupMenu667->CheckEntry(33);
   fPopupMenu667->AddEntry("&Resize Canvas",34);
   fPopupMenu667->AddEntry("&Move Opaque",35);
   fPopupMenu667->CheckEntry(35);
   fPopupMenu667->AddEntry("Resize &Opaque",36);
   fPopupMenu667->CheckEntry(36);
   fPopupMenu667->AddSeparator();
   fPopupMenu667->AddEntry("&Interrupt",37);
   fPopupMenu667->AddEntry("R&efresh",38);
   fPopupMenu667->AddSeparator();
   fPopupMenu667->AddEntry("&Pad Auto Exec",39);
   fPopupMenu667->AddSeparator();
   fPopupMenu667->AddEntry("&Statistics",40);
   fPopupMenu667->CheckEntry(40);
   fPopupMenu667->AddEntry("Histogram &Title",41);
   fPopupMenu667->CheckEntry(41);
   fPopupMenu667->AddEntry("&Fit Parameters",42);
   fPopupMenu667->AddEntry("Can Edit &Histograms",43);
   fMenuBar670->AddPopup("&Options",fPopupMenu667, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Tools" menu
   TGPopupMenu *fPopupMenu668 = new TGPopupMenu(gClient->GetDefaultRoot(),123,114,kOwnBackground);
   fPopupMenu668->AddEntry("&Inspect ROOT",44);
   fPopupMenu668->AddEntry("&Class Tree",45);
   fPopupMenu668->AddEntry("&Fit Panel",46);
   fPopupMenu668->AddEntry("&Start Browser",47);
   fPopupMenu668->AddEntry("&Gui Builder",48);
   fPopupMenu668->AddEntry("&Event Recorder",49);
   fMenuBar670->AddPopup("&Tools",fPopupMenu668, new TGLayoutHints(kLHintsLeft | kLHintsTop,0,4,0,0));

   // "Help" menu
   TGPopupMenu *fPopupMenu669 = new TGPopupMenu(gClient->GetDefaultRoot(),126,158,kOwnBackground);
   fPopupMenu669->AddLabel("Basic Help On...");
   fPopupMenu669->DefaultEntry(-1);
   fPopupMenu669->AddSeparator();
   fPopupMenu669->AddEntry("&Canvas",51);
   fPopupMenu669->AddEntry("&Menus",52);
   fPopupMenu669->AddEntry("&Graphics Editor",53);
   fPopupMenu669->AddEntry("&Browser",54);
   fPopupMenu669->AddEntry("&Objects",55);
   fPopupMenu669->AddEntry("&PostScript",56);
   fPopupMenu669->AddSeparator();
   fPopupMenu669->AddEntry("&About ROOT...",50);
   fMenuBar670->AddPopup("&Help",fPopupMenu669, new TGLayoutHints(kLHintsRight | kLHintsTop));
   fRootCanvas660->AddFrame(fMenuBar670, new TGLayoutHints(kLHintsLeft | kLHintsTop | kLHintsExpandX,0,0,1,1));
   TGHorizontal3DLine *fHorizontal3DLine678 = new TGHorizontal3DLine(fRootCanvas660,800,2);
   fRootCanvas660->AddFrame(fHorizontal3DLine678, new TGLayoutHints(kLHintsTop | kLHintsExpandX));

   // dockable frame
   TGDockableFrame *fDockableFrame679 = new TGDockableFrame(fRootCanvas660);

   // next lines belong to the dockable frame widget
   fDockableFrame679->EnableUndock(kTRUE);
   fDockableFrame679->EnableHide(kFALSE);
   fDockableFrame679->SetWindowName("ToolBar: frame_rrv_mass_lvj_34cefd90");
   fDockableFrame679->DockContainer();

   fRootCanvas660->AddFrame(fDockableFrame679, new TGLayoutHints(kLHintsExpandX));
   TGHorizontal3DLine *fHorizontal3DLine684 = new TGHorizontal3DLine(fRootCanvas660,800,2);
   fRootCanvas660->AddFrame(fHorizontal3DLine684, new TGLayoutHints(kLHintsTop | kLHintsExpandX));

   // composite frame
   TGCompositeFrame *fCompositeFrame685 = new TGCompositeFrame(fRootCanvas660,800,576,kHorizontalFrame);

   // composite frame
   TGCompositeFrame *fCompositeFrame686 = new TGCompositeFrame(fCompositeFrame685,175,576,kFixedWidth);
   fCompositeFrame686->SetLayoutManager(new TGVerticalLayout(fCompositeFrame686));

   fCompositeFrame685->AddFrame(fCompositeFrame686, new TGLayoutHints(kLHintsLeft | kLHintsExpandY));

   // canvas widget
   TGCanvas *fCanvas687 = new TGCanvas(fCompositeFrame685,800,576,kSunkenFrame);

   // canvas viewport
   TGViewPort *fViewPort688 = fCanvas687->GetViewPort();

   // canvas container
   Int_t canvasID = gVirtualX->InitWindow((ULong_t)fCanvas687->GetId());
   Window_t winC = gVirtualX->GetWindowID(canvasID);
   TGCompositeFrame *fCompositeFrame697 = new TGCompositeFrame(gClient,winC,fViewPort688);
   fViewPort688->AddFrame(fCompositeFrame697);
   fCompositeFrame697->SetLayoutManager(new TGVerticalLayout(fCompositeFrame697));
   fCompositeFrame697->MapSubwindows();
   fCanvas687->SetContainer(fCompositeFrame697);
   fCanvas687->MapSubwindows();
   fCompositeFrame685->AddFrame(fCanvas687, new TGLayoutHints(kLHintsRight | kLHintsExpandX | kLHintsExpandY));

   fRootCanvas660->AddFrame(fCompositeFrame685, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY));

   // status bar
   TGStatusBar *fStatusBar700 = new TGStatusBar(fRootCanvas660,10,18);
   Int_t partsusBar700[] = {33,10,10,47};
   fStatusBar700->SetParts(partsusBar700,4);
   fRootCanvas660->AddFrame(fStatusBar700, new TGLayoutHints(kLHintsLeft | kLHintsBottom | kLHintsExpandX,2,2,1,1));

   fRootCanvas660->SetWindowName("frame_rrv_mass_lvj_34cefd90");
   fRootCanvas660->SetIconName("frame_rrv_mass_lvj_34cefd90");
   fRootCanvas660->SetIconPixmap("macro_s.xpm");
   fRootCanvas660->SetClassHints("ROOT","Canvas");
   fRootCanvas660->SetMWMHints(kMWMDecorAll,
                        kMWMFuncAll,
                        kMWMInputModeless);
   fRootCanvas660->MapSubwindows();
   fHorizontal3DLine678->UnmapWindow();
   fDockableFrame679->UnmapWindow();
   fHorizontal3DLine684->UnmapWindow();
   fCompositeFrame686->UnmapWindow();
   fStatusBar700->UnmapWindow();

   fRootCanvas660->Resize(fRootCanvas660->GetDefaultSize());
   fRootCanvas660->MapWindow();
   fRootCanvas660->Resize(800,600);
}  
