## Multiplying on paper

Together as a class:

Graph a Square wave from `0 seconds` to `2 seconds` that has these attributes:

- When the wave is high, it is `1`.
- When the wave is low, it is `0`.
- Starts low.
- One full cycle (the **period**) is `1 seconds`.
- Question: What is the frequency?

Graph a Sin wave with a frequency of `4 Hz` across the same time range.

Now, multiply them.

## GNU Radio: Separate waves

After doing that on paper, implement in GNU Radio:

`square_wave_separate.grc`

```
Signal Source  -->  Time Sink

Signal Source  -->  Time Sink
```

- First Signal Source:
  - Output Type: `float`
  - Waveform: `Square`
  - Frequency: `1`
- Second Signal Source:
  - Output Type: `float`
  - Waveform: `Sine`
  - Frequency: `4`
- Time Sink (both):
  - Type: `Float`
- Variable (_already in the flowgraph_):
  - Id: `samp_rate`
  - Value: `100`

## GNU Radio: Multiplying

Now that we've seen the separate waves, let's multiply them:

`square_multiplied.grc`
```
Signal Source  -->  Multiply  -->  Time Sink
Signal Source  -->  
```

- First Signal Source:
  - Output Type: `float`
  - Waveform: `Square`
  - Frequency: `1`
- Second Signal Source:
  - Output Type: `float`
  - Waveform: `Sine`
  - Frequency: `4`
- Time Sink:
  - Type: `Float`
- Variable (_already in the flowgraph_):
  - Id: `samp_rate`
  - Value: `100`

### Exercises

1. What should the Square Wave frequency be if you want the signal to turn on for two seconds, and off for two seconds? _Hint: Try `2` and `0.5`. Neither is the correct answer, but those may help you find the answer._
2. How would you make the Sine wave's frequency slideable between 2 Hz and 20 Hz?
3. Once you've set up that slider, try some other frequencies for the Sine wave to see what they look like. For example, try `10` and `20`. 
