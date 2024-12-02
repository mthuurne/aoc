use std::{env, fs::File, io, io::BufRead, iter::zip, path::Path};

fn read_input(path: &Path) -> io::Result<Vec<(i64, i64)>> {
    let file = File::open(path)?;
    let mut data: Vec<(i64, i64)> = Vec::new();
    for line in io::BufReader::new(file).lines() {
        let values = Vec::from_iter(line?.split_whitespace().map(
            |s| s.parse().expect("values must be integers")
        ));
        match &values[..] {
            &[first, second, ..] => data.push((first, second)),
            _ => panic!("input must have two values per line"),
        };
    }
    Ok(data)
}

fn solve(data: &Vec<(i64, i64)>) {
    let (mut l1, mut l2): (Vec<_>, Vec<_>) = data.iter().cloned().unzip();
    l1.sort();
    l2.sort();
    let total_delta: i64 = zip(l1, l2).map(|(x1, x2)| (x1 - x2).abs()).sum();
    println!("{total_delta}");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    for arg in &args[1..] {
        println!("=== {arg}");
        let data = read_input(Path::new(arg)).expect("reading input");
        solve(&data);
    }
}
