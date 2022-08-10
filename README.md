# MPI-IE Slurm Profile

> A simple Snakemake profile for the MPI-IE Slurm cluster without `--cluster-config`

* [Features](#features)
* [Limitations](#limitations)
* [Quick start](#quick-start)
* [Customizations](#customizations)
* [Use speed with caution](#use-speed-with-caution)
* [License](#license)

This is a fork of the excellent [smk-simple-slurm][] Snakemake profile, which
itself is a simplified version of the more comprehensive [official Slurm
profile for Snakemake][slurm-official].

## Features

* Support for stopping Snakemake with Ctrl-C, which then propagates `scancel`
  to children jobs using `--cluster-cancel`

* Support for Snakemake understanding job statuses PENDING, RUNNING, COMPLETING,
  OUT_OF_MEMORY, TIMEOUT, and CANCELLED using `--cluster-status`. NB:
  as of 2022-08-10 `sacct` does not work on the MPI-IE slurm cluster as of now,
  so this uses `scontrol` instead.

* Automatically saves the log files as `logs/{date}/{rule}/{rule}-{wildcards}-{time}-job%j.out`,
  where `{rule}` is the name of the rule, `{wildcards}` is any wildcards passed
  to the rule, `{date}` and `{time}` are determined dynamically and `%j` is the
  job number.

* automatically load slurm module for MPI-IE cluster in relevant places

* use `/data/extended` as the default tmpdir and export this as TMPDIR variable

* automatically names jobs according to their rule

* Fast! It can quickly submit jobs and check their status because it doesn't
  invoke a Python script for these steps, which adds up when you have thousands
  of jobs (however, please see the section [Use speed with
  caution](#use-speed-with-caution))

* No reliance on the deprecated option `--cluster-config` to customize job
  resources

* If you wish to add more features, see the original [smk-simple-slurm][] profile or
  [official SLURM profile][slurm-official] for inspiration.

## Limitations

* Can't use [group jobs][grouping], but they [aren't easy to use in the first
  place][grouping-issue]

* Wildcards can't contain `/` if you want to use them in the name of the Slurm
  log file. This is a Slurm requirement (which makes sense, since it has to
  create a file on the filesystem). You'll either have to change how you manage
  the wildcards or remove the `{wildcards}` from the pattern passed to `--output`,
  e.g. `--output=logs/{rule}/{rule}-%j.out`.
  Note that you can still submit wildcards containing `/` to `--job-name`

* Requires Snakemake version 7.0.0 or later (for `--cluster-cancel`).
  You can test this directly in your `Snakefile` with [`min_version()`][min_version]

## Quick start

1. Copy the directory `mpi-ie-slurm` to a directory of your choice.

2. Edit any variables in `config.yaml` if you wish.

3. You can override any of the defaults by adding a `resources` field to a rule,
   e.g.

    ```python
    rule much_memory:
        resources:
            mem_mb=64000
    ```

4. Invoke snakemake with the profile:

    ```sh
    snakemake --profile mpi-ie-slurm/
    ```

## Use speed with caution

A big benefit of the simplicity of this profile is the speed in which jobs can
be submitted and their statuses checked. The [official Slurm profile for
Snakemake][slurm-official] provides a lot of extra fine-grained control, but
this is all defined in Python scripts, which then have to be invoked for each
job submission and status check. I needed this speed for a pipeline that had an
aggregation rule that needed to be run tens of thousands of times, and the run
time for each job was under 10 seconds. In this situation, the job submission
rate and status check rate were huge bottlenecks.

However, you should use this speed with caution! On a shared HPC cluster, many
users are making requests to the Slurm scheduler. If too many requests are made
at once, the performance will suffer for all users. If the rules in your
Snakemake pipeline take at least more than a few minutes to complete, then it's
overkill to constantly check the status of multiple jobs in a single second. In
other words, only increase `max-jobs-per-second` and/or
`max-status-checks-per-second` if either the submission rate or status checks to
confirm job completion are clear bottlenecks.

## License

This is all boiler plate code. Please feel free to use it for whatever purpose
you like. No need to attribute or cite this repo, but of course it comes with no
warranties. To make it official, it's released under the [CC0][] license. See
[`LICENSE`](LICENSE) for details.

[aws-parallelcluster]: https://aws.amazon.com/hpc/parallelcluster/
[cbrueffer]: https://github.com/cbrueffer
[CC0]: https://creativecommons.org/publicdomain/zero/1.0/
[changelog]: https://snakemake.readthedocs.io/en/stable/project_info/history.html
[cluster-cancel]: https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#using-cluster-cancel
[cluster-config]: https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html#cluster-configuration-deprecated
[cluster-execution]: https://snakemake.readthedocs.io/en/stable/executing/cluster.html
[cluster-status]: https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#using-cluster-status
[grouping]: https://snakemake.readthedocs.io/en/stable/executing/grouping.html
[grouping-issue]: https://github.com/snakemake/snakemake/issues/872
[min_version]: https://snakemake.readthedocs.io/en/stable/snakefiles/writing_snakefiles.html#depend-on-a-minimum-snakemake-version
[multi_cluster]: https://slurm.schedmd.com/multi_cluster.html
[no-cluster-status]: http://bluegenes.github.io/Using-Snakemake_Profiles/
[sichong-post]: https://www.sichong.site/workflow/2021/11/08/how-to-manage-workflow-with-resource-constraint.html
[slurm-official]: https://github.com/Snakemake-Profiles/slurm
[smk-simple-slurm]: https://github.com/jdblischak/smk-simple-slurm
[snakemake-aws-parallelcluster-slurm]: https://github.com/cbrueffer/snakemake-aws-parallelcluster-slurm
