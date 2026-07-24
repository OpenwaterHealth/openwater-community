# Hardware setup

This document covers the physical setup for a closed-loop LIFU–EEG session and the
installation of the proprietary g.Pipe SDK.

> **Research use only.** This describes a research bench setup, not a clinical procedure.

---

## Bill of materials

| Item | Notes |
|------|-------|
| g.tec EEG amplifier + electrode set | The reference amplifier for this implementation |
| g.Pipe SDK | **Proprietary, user-supplied** — see [Installing the g.Pipe SDK](#installing-the-gpipe-sdk) |
| EEG cap | Sized to the subject |
| Conductive gel | For electrode–scalp impedance |
| OpenLIFU transducer + drive hardware | Per the OpenLIFU platform documentation |
| Acoustic coupling medium | For LIFU–scalp coupling |
| Host computer | Runs acquisition, task, trigger, and LIFU control over LSL |

---

## Headset + LIFU co-placement

The EEG cap and the LIFU transducer share scalp real estate, so placement has to be
planned so that neither compromises the other:

- Place the EEG cap first and establish acceptable electrode impedances with gel.
- Position the LIFU transducer at the intended target with its coupling medium, taking
  care not to disturb or bridge nearby electrodes.
- Verify that electrodes adjacent to the transducer still read acceptable impedance
  after the transducer and coupling medium are in place — coupling medium contacting an
  electrode is a common source of artefact.
- Confirm the EEG stream is clean (visually and via the artifact-gating flag rate)
  *before* starting calibration.

> [!NOTE]
> This pipeline does **not** perform MRI-guided targeting or acoustic skull correction.
> Transducer placement is manual and anatomical. Those are tracked as open enhancement
> items in [`known-issues.md`](known-issues.md) and are design decisions for the
> platform owners, not something this feasibility implementation resolves.

---

## Installing the g.Pipe SDK

The g.Pipe SDK is **proprietary software from g.tec** and **cannot be redistributed or
vendored** in this repository. You must obtain and install it yourself under your own
license from g.tec.

1. Obtain the g.Pipe SDK and license from g.tec.
2. Install it per g.tec's instructions for your platform.
3. Make the SDK importable in the environment where you run this pipeline (e.g. on the
   `PYTHONPATH`, or installed into the same virtual environment).
4. Verify the acquisition adapter can import it:

   ```bash
   python -c "import openlifu_closed_loop.acquisition as a; a.check_gpipe()"
   ```

If you use a **different amplifier**, you do not need the g.Pipe SDK. Implement the
acquisition interface for your hardware instead (see
[`architecture.md`](architecture.md#module-boundaries)) — this is an explicitly
supported extension point, and adapter contributions are welcome.

---

## Sanity check before a session

- [ ] EEG stream present on LSL and timestamps advancing
- [ ] Electrode impedances acceptable, including electrodes adjacent to the transducer
- [ ] Artifact-gating flag rate low on resting subject
- [ ] Task (PsychoPy 2-back) launches and publishes markers to LSL
- [ ] LIFU control reachable; run once in `--dry-run` to confirm the trigger→LIFU path
      logs decisions without issuing sonications
- [ ] Logging is writing to the intended output location
