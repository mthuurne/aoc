use std::{env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<Vec<(u64, Vec<u64>)>> {
    let file = File::open(path)?;

    let mut equations = Vec::new();
    for line in io::BufReader::new(file).lines() {
        let text = line?;
        let mut parts = text.split_whitespace();
        let target = parts.next().unwrap().trim_end_matches(':').parse().expect("integer");
        let values = parts.map(|s| s.parse().expect("integer")).collect();
        equations.push((target, values));
    }

    Ok(equations)
}

fn concat(a: u64, b: u64) -> u64 {
    let mut shifted = a;
    let mut remainder = b;
    loop {
        shifted *= 10;
        remainder /= 10;
        // Loop at least once to handle b == 0 correctly.
        if remainder == 0 { break }
    }
    shifted + b
}

fn rec_match(total: u64, target: u64, remaining: &[u64]) -> bool {
    if remaining.is_empty() {
        total == target
    } else if total > target {
        // Our operators can only increase the total, so we can't match from here.
        false
    } else {
        rec_match(total * remaining[0], target, &remaining[1..]) ||
        rec_match(total + remaining[0], target, &remaining[1..]) ||
        rec_match(concat(total, remaining[0]), target, &remaining[1..])
    }
}

fn can_match(target: u64, values: &Vec<u64>) -> bool {
    rec_match(values[0], target, &values.as_slice()[1..])
}

fn solve(equations: Vec<(u64, Vec<u64>)>) {
    let total: u64 = equations.iter().map(|(target, values)| if can_match(*target, values) { *target } else {0}).sum();
    println!("{total}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let equations = read_input(Path::new(&arg)).expect("reading input");
        solve(equations);
    }
}
