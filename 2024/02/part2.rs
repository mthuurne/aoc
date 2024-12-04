use itertools::Itertools;
use std::{env, fs::File, io, io::BufRead, iter::FromIterator, iter::Iterator, iter::ExactSizeIterator, path::Path};

fn read_input(path: &Path) -> io::Result<Vec<Vec<i64>>> {
    let file = File::open(path)?;
    let mut data: Vec<Vec<i64>> = Vec::new();
    for line in io::BufReader::new(file).lines() {
        let values = Vec::from_iter(line?.split_whitespace().map(
            |s| s.parse().expect("values must be integers")
        ));
        data.push(values);
    }
    Ok(data)
}

fn is_slow_increase<'a>(it: impl Iterator<Item=&'a i64>) -> bool {
    it.tuple_windows().all(|(x1, x2)| {
        let d = x2 - x1; 1 <= d && d <= 3
    })
}

fn is_slow_increase_after_dampening<'a>(it: impl ExactSizeIterator<Item=&'a i64> + Clone) -> bool {
    (0..it.len()).any(|skip|
        is_slow_increase(it.clone().enumerate().filter_map(|(idx, val)|
            if idx == skip { None } else { Some(val) }
        ))
    ) || is_slow_increase(it)
}

fn solve(reports: &Vec<Vec<i64>>) {
    let num_safe = reports.iter().filter(|report|
        is_slow_increase_after_dampening(report.iter()) ||
        is_slow_increase_after_dampening(report.iter().rev())
    ).count();
    println!("{num_safe}");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    for arg in &args[1..] {
        println!("=== {arg}");
        let data = read_input(Path::new(arg)).expect("reading input");
        solve(&data);
    }
}
