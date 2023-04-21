# YoYo_Judge
Base yoyo tracker by [hanlinm2](https://github.com/hanlinm2/yoyo_tracking_vfx).

This is the initial version of an yoyo judge based on an existing yoyo tracking project. The yoyo judge operates under the assumption that a yoyo trick scores if it makes contact with the string. However, the initial version is unable to track the string yet. Thus we use the change of velocity as a simulated metric for contact with the string, since yoyo velocity changes dramatically when there is contact with the string. Depending on the player, you might need to modify the threshold for velocity change.

## Running the Project

To run the project, use the following command:

```python3 yoyo_tracker_judge.py```

## Dependencies

The project uses `CV2` version `4.7.0`.

## Future Development

Future development will focus on figuring out how to track or detect the string.
