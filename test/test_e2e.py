import os
import subprocess

def test_ankrd11_example(tmpdir):
    """make sure the ankrd11 example works
    compares the first 6 lines of the output to what is expected
    """
    bash_file = os.path.join(os.path.dirname(__file__), '..', 'example', 'ANKRD11example.sh')
    bash_command = f"bash {bash_file}"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tVPS13B\t157680\t1.0\tSeedGene",
        "2\tANKRD11\t29123\t0.957522\tSeedGene",
        "3\tALDH7A1\t501\t0.859035\tSeedGene",
        "4\tNHLRC1\t378884\t0.805299\tSeedGene",
        "5\tALDH5A1\t7915\t0.79442\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'ankrd11', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])


def test_input_file_example():
    """make sure the input file example works
    compares the first 6 lines of the output to what is expected
    """
    bash_command = "python phen2gene.py -f example/HPO_sample.txt -out out/prioritizedgenelist"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tELN\t2006\t1.0\tSeedGene",
        "2\tHDAC8\t55869\t0.632013\tSeedGene",
        "3\tSMC1A\t8243\t0.625186\tSeedGene",
        "4\tSMC3\t9126\t0.60777\tSeedGene",
        "5\tLIMK1\t3984\t0.588771\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'out', 'prioritizedgenelist', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])


def test_input_file_w_candidate_gene_list_example():
    """make sure the input file with candidate gene list example works
    compares the first 6 lines of the output to what is expected
    """
    bash_command = "python phen2gene.py -f example/HPO_sample.txt -out out/prioritizedgenelist2 -l example/1000genetest.txt"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tRAD21\t5885\t1.0\tSeedGene",
        "2\tTAF1\t6872\t0.828886\tSeedGene",
        "3\tMAP2K1\t5604\t0.501661\tSeedGene",
        "4\tPSMD12\t5718\t0.495574\tSeedGene",
        "5\tSMARCE1\t6605\t0.489454\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'out', 'prioritizedgenelist2', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])


def test_manual_hpo_example():
    """make sure the manual HPO example works
    compares the first 6 lines of the output to what is expected
    """
    bash_command = "python phen2gene.py -m HP:0000021 HP:0000027 HP:0030905 HP:0010628 -out out/prioritizedgenelistmanual"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tCHD7\t55636\t1.0\tSeedGene",
        "2\tBLM\t641\t0.964734\tSeedGene",
        "3\tHFE\t3077\t0.51236\tSeedGene",
        "4\tSEMA3E\t9723\t0.480512\tSeedGene",
        "5\tSOST\t50964\t0.467741\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'out', 'prioritizedgenelistmanual', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])


def test_weighting_example_sk():
    """make sure the -w sk weighting option works
    compares the first 6 lines of the output to what is expected
    """
    bash_command = "python phen2gene.py -f example/HPO_sample.txt -w sk -out out/prioritizedgenelistsk"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tELN\t2006\t1.0\tSeedGene",
        "2\tHDAC8\t55869\t0.632013\tSeedGene",
        "3\tSMC1A\t8243\t0.625186\tSeedGene",
        "4\tSMC3\t9126\t0.60777\tSeedGene",
        "5\tLIMK1\t3984\t0.588771\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'out', 'prioritizedgenelistsk', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])


def test_weighting_example_ic():
    """make sure the -w ic weighting option works
    compares the first 6 lines of the output to what is expected
    """
    bash_command = "python phen2gene.py -f example/HPO_sample.txt -w ic -out out/prioritizedgenelistic"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tELN\t2006\t1.0\tSeedGene",
        "2\tDHCR7\t1717\t0.730837\tSeedGene",
        "3\tFGFR3\t2261\t0.726738\tSeedGene",
        "4\tHDAC8\t55869\t0.718541\tSeedGene",
        "5\tSMC1A\t8243\t0.694527\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'out', 'prioritizedgenelistic', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])


def test_weighting_example_w():
    """make sure the -w w weighting option works
    compares the first 6 lines of the output to what is expected
    """
    bash_command = "python phen2gene.py -f example/HPO_sample.txt -w w -out out/prioritizedgenelistw"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tELN	2006\t1.0\tSeedGene",
        "2\tHDAC8\t55869\t0.681365\tSeedGene",
        "3\tSMC3\t9126\t0.64701\tSeedGene",
        "4\tSMC1A\t8243\t0.644281\tSeedGene",
        "5\tFGFR2\t2263\t0.631136\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'out', 'prioritizedgenelistw', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])


def test_weighting_example_u():
    """make sure the -w u weighting option works
    compares the first 6 lines of the output to what is expected
    """
    bash_command = "python phen2gene.py -f example/HPO_sample.txt -w u -out out/prioritizedgenelistu"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    expected = [
        "Rank\tGene\tID\tScore\tStatus",
        "1\tELN\t2006\t1.0\tSeedGene",
        "2\tFGFR3\t2261\t0.779641\tSeedGene",
        "3\tDHCR7\t1717\t0.754031\tSeedGene",
        "4\tHDAC8\t55869\t0.701246\tSeedGene",
        "5\tTCF4\t6925\t0.695881\tSeedGene"
    ]
    with open(os.path.join(os.path.dirname(__file__), '..', 'out', 'prioritizedgenelistu', 'output_file.associated_gene_list')) as f:
        for i in range(len(expected)):
            line = next(f).strip()
            assert(line == expected[i])
