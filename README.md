# rtpt

RTPT class to rename your processes giving information on who is launching the
process, and the remaining time for it.
Created to be used with our AIML IRON table.

## Example
    rtpt = RTPT(base_title='UserName', number_of_epochs=num_epochs, epoch_n=0)
    for epoch in range(num_epochs):
      rtpt.epoch_starts()
      train()
      test()
      rtpt.setproctitle()
