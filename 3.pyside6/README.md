# ProjectPySide

## Task
Stop Motion Player의 완성

## Requirements
01. Your player should have a region that plays the video
02. Your player should have a playlist manager
03. A user may add the stop motion video
04. A user may remove the stop motion video
05. A user may change order of a stop motion video
06. Your player should have a control buttons for play, pause, resume, stop
07. If a user clicks the play button, the player should play the stop motion animation
08. After clicking pause, the player should pause the stop motion animation
09. When the user clicks the resume button, the player should play the animation from paused point
10. After the user clicks the stop button, the player will play the first stop motion animation of the player list.

## Snapshot
![2022-10-05_14-55-33](https://user-images.githubusercontent.com/10826491/193991246-39343c10-f39b-44b4-b873-141d3d0e9b4a.gif)

## Hints
### Component Candidates
 - QTimer
 
### Functino Candidates
- Function Candidates
  - QListWidget::itemActivated
    * To indicate which list item is activated
  - QListWidget::currentRow
    * To indicate the current row
  - QListWidget::addItem
    * To insert an item to the playlist
  - QListWidget::takeItem
    * To remove an item from the playlist
  - QListWidget::setCurrentItem
    * To set a value of an item
  - QListWidget::item
    * To retrieve the value from an item
